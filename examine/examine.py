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
        self.type_ = type(value)
        self.key_guaranteed = True
        self.val_guaranteed = True
        self.children = []

        if self.is_list:
            # Make a structure out of each item in the list
            list_items = [Structure(item, parent=self) for item in value]
            if list_items:
                # Add all structures together to get the common structure
                merged_structure = list_items[0]
                for item in list_items[1:]:
                    merged_structure += item
                # Set the only list child to the common structure
                self.children.append(merged_structure)
            else:
                self.children.append(Structure(_EMPTY_TYPE(), parent=self))
        elif self.is_tuple:
            # Make a structure out of each item in the tuple
            tuple_items = [Structure(item, parent=self) for item in value]
            if tuple_items:
                self.children = tuple_items
            else:
                self.children.append(Structure(_EMPTY_TYPE(), parent=self))
        elif self.is_dict:
            for key, val in value.items():
                self.children.append(Structure(val, key, self))
            self.children.sort(key=lambda child: child.key)

    def __add__(self, other):
        assert self.key == other.key

        new = Structure(None, key=self.key)
        new.key_guaranteed = self.key_guaranteed & other.key_guaranteed
        new.val_guaranteed = self.val_guaranteed & other.val_guaranteed
        # if one has a non-guaranteed value, the other can't either
        # self.key_guaranteed &= other.key_guaranteed
        # self.val_guaranteed &= other.val_guaranteed

        if self.is_list and other.is_list:
            new.type_ = list
            listchild = self.children[0] + other.children[0]
            listchild.parent = new
            new.children.append(listchild)
            s_child = self.children[0]
            o_child = other.children[0]
            return new
            # if s_child.type_ is _EMPTY_TYPE:
            #     return other
            # elif o_child.type_ is _EMPTY_TYPE:
            #     return self
            # elif s_child.type_ is _NONE_TYPE:
            #     if o_child.type_ is not _NONE_TYPE:
            #         o_child.val_guaranteed = False
            #     o_child.parent = self
            #     self.children[0] = o_child
            #     return self
            # elif o_child.type_ is _NONE_TYPE:
            #     if s_child.type_ is not _NONE_TYPE:
            #         s_child.val_guaranteed = False
            #     return self
            # elif s_child.type_ is o_child.type_:
            #     self.children[0] += other.children[0]
            #     return self
            # else:
            #     self.children[0].type_ = _MIXED_TYPE
            #     self.children[0].childern = []
            #     return self
        elif self.is_tuple and other.is_tuple:
            # Run through each child of the two tuples, in order, and where
            # there is a difference, indicate <mixed>

            # If tuple lengths are not the same, indicate the extra length
            # children are not guaranteed
            return self
        elif self.is_dict and other.is_dict:
            return self
        elif self.type_ is other.type_:
            return self
        else:
            if self.type_ is _NONE_TYPE:
                self.type_ = other.type_
                self.val_guaranteed = False
                self.children = other.children
                for child in self.children:
                    child.parent = self
            elif other.type_ is _NONE_TYPE:
                self.val_guaranteed = False
            else:
                self.type_ = _MIXED_TYPE
                self.children = []
            return self

    def __contains__(self, item):
        for child in self.children:
            if child.key == item.key:
                return True
        return False

    def __str__(self):
        if self.parent:
            string = '{}{} - {}\n'.format(
                '  ' * (self.generation - 1),
                self.key,
                self.type_string)
        else:
            string = '=== {} ===\n'.format(self.type_string)
        if self.children and self.type_ is dict:
            for child in self.children:
                string += str(child) + '\n'
        return string[:-1]

    @property
    def generation(self):
        if not self.parent:
            return 0
        elif self.is_list or self.is_tuple:
            return self.parent.generation
        else:
            return 1 + self.parent.generation

    @property
    def type_string(self):
        if self.is_tuple:
            subtypes = [item.type_string for item in self.children]
            return '{}({})'.format(
                '' if self.val_guaranteed else '*',
                ', '.join(subtypes))
        elif self.is_list:
            return '{}[{}]'.format(
                '' if self.val_guaranteed else '*',
                self.children[0].type_string)
        else:
            return '{}{}'.format(
                '' if self.val_guaranteed else '*',
                self.type_.__name__)
    
    @property
    def is_list(self):
        return issubclass(self.type_, list)

    @property
    def is_tuple(self):
        return issubclass(self.type_, tuple)

    @property
    def is_dict(self):
        return issubclass(self.type_, dict)
    