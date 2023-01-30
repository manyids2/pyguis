from typing import List, Mapping, Optional, Any, Dict, Union
from pathlib import Path
from argparse import Namespace

import json
import yaml
import pickle


def subdirs(dir_: Path) -> List[str]:
    return [d.name for d in dir_.iterdir() if d.is_dir()]


def flatten_list(list_: list) -> list:
    flat_list = [item for sublist in list_ for item in sublist]
    return flat_list


def dict_to_namespace(dict_: Dict, vtype: Optional[Any] = None) -> Namespace:
    def recurse(_dict):
        # If all children are not dicts
        ret = {}
        for k, v in _dict.items():
            if isinstance(v, dict):
                ret[k] = recurse(v)
            else:
                if vtype is not None:
                    ret[k] = vtype(v)
                else:
                    ret[k] = v
        return Namespace(**ret)

    return recurse(dict_)


def namespace_to_dict(namespace: Namespace) -> Dict:
    def recurse(_ns):
        # If all children are not dicts
        ret = {}
        for k, v in _ns.__dict__.items():
            if isinstance(v, Namespace):
                ret[k] = recurse(v)
            else:
                ret[k] = v
        return ret

    return recurse(namespace)


def save_dict(dict_: Dict, fname: Union[str, Path]) -> None:
    with open(str(fname), "wb") as f:
        pickle.dump(dict_, f)


def load_dict(fname: Union[str, Path]) -> Dict:
    with open(str(fname), "rb") as f:
        ret_dict = pickle.load(f)
    return ret_dict


def save_yaml(dict_: Mapping[Any, Any], fname: Union[str, Path]) -> None:
    with open(fname, "w") as fp:
        yaml.dump(dict_, fp, sort_keys=False)


def load_yaml(fname: Union[str, Path]) -> Dict[Any, Any]:
    with open(str(fname), "r") as fp:
        data = yaml.load(fp, Loader=yaml.FullLoader)
    return data


def load_json(fname: Union[str, Path]) -> Dict:
    with open(str(fname)) as fp:
        data = json.load(fp)
    return data


def save_json(dict_: Dict, fname: Union[str, Path]) -> None:
    Path(fname).write_text(json.dumps(dict_))
