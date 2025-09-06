import os
import h5py
import numpy as np

class Serializable:
    def __str__(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items() if value is not None]
        return "\n".join(attributes)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for key in self.__dict__.keys():
            if isinstance(self.__dict__[key], np.ndarray):
                if not np.allclose(self.__dict__[key], other.__dict__[key]):
                    return False
            elif self.__dict__[key] != other.__dict__[key]:
                return False
        return True

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._init_params = list(kwargs.keys())
        return instance

    def serialize(self):
        initdata = {key: value for key, value in self.__dict__.items() if key in self._init_params}
        return initdata

    def write_to_file(self, filepath, data_dict):
        with h5py.File(filepath, 'w') as f:
            for key, value in data_dict.items():
                f.create_dataset(key, data=value)
            f.attrs['class'] = self.__class__.__name__
            f.attrs['init_params'] = self._init_params
            for param in self._init_params:
                f.attrs[param] = self.__dict__[param]

def generate_file_path(extension, file_name, path):
    if not os.path.exists(path):
        os.makedirs(path)
    existing_files = [f for f in os.listdir(path) if f.startswith(file_name) and f.endswith(extension)]
    if existing_files:
        max_prefix = max([int(f.split('_')[0]) for f in existing_files])
        new_prefix = max_prefix + 1
    else:
        new_prefix = 1
    new_file_name = f"{str(new_prefix).zfill(3)}_{file_name}.{extension}"
    return os.path.join(path, new_file_name)

def read_from_file(filepath):
    with h5py.File(filepath, 'r') as f:
        class_name = f.attrs['class']
        init_params = f.attrs['init_params']
        data_dict = {key: f[key][()] for key in f.keys()}
        class_module = __import__(class_name.lower())
        class_ = getattr(class_module, class_name)
        init_kwargs = {param: f.attrs[param] for param in init_params}
        new_class_instance = class_(**init_kwargs)
        return new_class_instance, data_dict

def get_init_params(obj):
    return list(obj._init_params)