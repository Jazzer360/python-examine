_NONE_TYPE = type(None)
_EMPTY_TYPE = type('', (object,), {})
_MIXED_TYPE = type('<mixed-type>', (object,), {})


class AttrDict(dict):
    """A dict with keys accessible as attributes."""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Structure(object):
    """An object that reflects the structure of any python data structure.

    Any object may be passed to the constructor and a complete traverse
    of the structure occurs, making all the appropriate links so that
    a simple hierarchy may be retrieved. The str function will turn these
    objects into a simple hierarchy with notations for lists and whether or
    not an attribute will be guaranteed for each particular branch. Also
    supported is adding different Structure objects, which will show only
    the structure common to both. Wherever the structure differs, it will
    be noted as a '<mixed-type>'
    """
    def __init__(self, value, key=None, parent=None):
        self.key = key
        self.parent = parent
        self.valtype = type(value)
        self.key_guaranteed = True
        self.val_guaranteed = True
        self.children = []
        self.list_depth = 0

        if isinstance(value, list):
            # Make a structure out of each list item
            list_items = [Structure(item) for item in value]
            if list_items:
                # Merge each structure in the list
                merged_hierarchy = list_items[0]
                for item in list_items[1:]:
                    merged_hierarchy += item
                # Make this structure the same as the merged structure
                self.list_depth = merged_hierarchy.list_depth + 1
                self.valtype = merged_hierarchy.valtype
                self.val_guaranteed = merged_hierarchy.val_guaranteed
                self.children = merged_hierarchy.children
                for child in self.children:
                    child.parent = self
            # The list didn't have anything, but is still a list
            else:
                self.list_depth = 1
                self.valtype = _EMPTY_TYPE
        elif isinstance(value, dict):
            self.children = []
            for key, val in value.items():
                self.children.append(Structure(val, key, self))

        if self.children:
            self.children.sort(key=lambda child: child.key)

    def __add__(self, other):
        # It only makes sense to add attributes with same parent/key
        if self.parent != other.parent:
            raise ValueError('You may only sum attributes that share a parent')
        elif self.key != other.key:
            raise ValueError('You may only sum attributes with equal keys')
        # When dealing with a list of some type and an empty list, allow
        # them to merge.
        if ((self.list_depth or other.list_depth) and
            self.list_depth == other.list_depth):
                if self.valtype and other.valtype is _EMPTY_TYPE:
                    return self
                elif other.valtype and self.valtype is _EMPTY_TYPE:
                    return other
        # First check if one of the types is None, and defer to other
        if self.valtype == _NONE_TYPE and other.valtype == _NONE_TYPE:
            self.val_guaranteed &= other.val_guaranteed
            return self
        elif (self.valtype == _NONE_TYPE and
            self.list_depth == other.list_depth):
                self.valtype = other.valtype
                self.val_guaranteed = False
        elif (other.valtype == _NONE_TYPE and
            self.list_depth == other.list_depth):
                other.valtype = self.valtype
                self.val_guaranteed = False
        # If types don't match, indicate mixed and clear children
        if (self.valtype != other.valtype or
            self.list_depth != other.list_depth):
                self.valtype = _MIXED_TYPE
                self.children = []
                self.list_depth = 0
        # If both have children merge them and indicate guaranteed
        elif self.children and other.children:
            for c1 in self.children:
                key_guaranteed = False
                for c2 in other.children:
                    if c1.key == c2.key:
                        c2.parent = c1.parent
                        c1 += c2
                        key_guaranteed = c1.key_guaranteed
                c1.key_guaranteed = key_guaranteed
            for child in other.children:
                if child not in self:
                    self.children.append(child)
                    child.parent = self
                    child.key_guaranteed = False
        # If only self has children indicate they're not guaranteed
        elif self.children and not other.children:
            for child in self.children:
                child.key_guaranteed = False
        # If only other has children indicate they're not guaranteed
        elif other.children and not self.children:
            self.children = other.children
            for child in self.children:
                child.key_guaranteed = False
                child.parent = self
        return self

    def __contains__(self, item):
        for child in self.children:
            if child.key == item.key:
                return True
        return False

    def __str__(self):
        if self.parent:
            string = '{}{}{} - {}{}{}{}\n'.format(
                '  ' * (self.generation - 1),
                '' if self.key_guaranteed else '*',
                self.key,
                self.list_depth * '[',
                '' if self.val_guaranteed else '*',
                self.valtype.__name__,
                self.list_depth * ']')
        else:
            string = '=== {}{}{}{} ===\n'.format(
                self.list_depth * '[',
                '' if self.val_guaranteed else '*',
                self.valtype.__name__,
                self.list_depth * ']')
        if self.children:
            for child in self.children:
                string += str(child) + '\n'
        return string[:-1]

    @property
    def generation(self):
        if not self.parent:
            return 0
        return 1 + self.parent.generation

