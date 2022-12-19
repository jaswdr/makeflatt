class NotADictionaryException(Exception):
    def __init__(self, data) -> None:
        super().__init__(f"Expected a dictionary, got {type(data)}")


class FlattMaker:
    def __init__(self, sep=".") -> None:
        self.sep = sep

    def _make_flat(self, data: dict, parent_key: str = "", include_lists: bool = False):
        items = []
        for k, v in data.items():
            new_key = parent_key + self.sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    self._make_flat(v, new_key, include_lists=include_lists).items()
                )
            elif isinstance(v, list) and include_lists:
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        items.extend(
                            self._make_flat(
                                v[i],
                                new_key + self.sep + str(i),
                                include_lists=include_lists,
                            ).items()
                        )
                    else:
                        items.append((new_key + self.sep + str(i), v[i]))
            else:
                items.append((new_key, v))
        return dict(items)

    def apply(self, data: dict, include_lists: bool = True):
        if isinstance(data, dict):
            return self._make_flat(data, include_lists=include_lists)

        raise NotADictionaryException(data)
