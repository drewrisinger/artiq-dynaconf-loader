"""Load ARTIQ Datasets into :mod:`dynaconf`."""
import pathlib

import artiq.protocols.pc_rpc as artiq_connection
import artiq.protocols.pyon as pyon
import dynaconf


def load(
    obj: dynaconf.LazySettings,
    env: str = None,
    silent: bool = True,
    key: str = None,
    filename: str = None,
) -> None:
    """
    Read and load in to `obj` a single key or all keys from ARTIQ datasets.

    If you would like different name mappings, they need to be specified
    in a settings file (either set as an environment variable TODO,
    or defaults to TODO).
    This defaults to connecting to an ARTIQ master instance on the local machine,
    but can be changed with the environment variable: TODO

    Args:
        obj (dynaconf.LazySettings): the settings instance
        env (str): settings current env (upper case) default='DEVELOPMENT'
        silent (bool): if errors should raise
        key (str): if defined load a single key, else load all from `env`
        filename (str): Custom filename to load (useful for tests)

    Returns:
        None

    """
    # pylint: disable=unused-argument
    # REQUIRED FILES:
    #   ? ARTIQ config settings (master IP address)??
    #   ? ARTIQ dataset mappings to variable names?? Env var?
    # Load data from your custom data source (file, database, memory etc)
    # use `obj.set(key, value)` or `obj.update(dict)` to load data
    # use `obj.logger.debug` to log your loader activities
    # use `obj.find_file('filename.ext')` to find the file in search tree
    # Return nothing

    port = 3250
    ip = "::1"
    # TODO: make ip, port, mapping_file to be dynamic-set

    mapping_file_path = pathlib.Path(obj.find_file("artiq_dataset_map.pyon"))
    if mapping_file_path.exists() and mapping_file_path.is_file():
        obj.logger.debug("Using key mapping file `%s`")
        key_to_dataset_map = pyon.decode(obj.read_file(mapping_file_path))
        dynaconf_keys = list(sorted(key_to_dataset_map.keys()))
        if key is not None and key in dynaconf_keys:
            dynaconf_keys = [key]
        elif key is not None:
            # TODO: handle silent
            raise KeyError(
                "Key {} not in ARTIQ mapping file {}".format(key, mapping_file_path)
            )
        try:
            artiq_datasets = artiq_connection.Client(
                ip, port, "master_dataset_db", timeout=10
            )
            dynaconf_values = list(artiq_datasets.get(k) for k in dynaconf_keys)
        finally:
            artiq_datasets.close_rpc()
        obj.update(dict(zip(dynaconf_keys, dynaconf_values)))
    else:
        # TODO
        if silent:
            obj.logger.debug("Key mapping file not found. Cannot load ARTIQ datasets")
        else:
            raise NotImplementedError(
                "Loading ARTIQ datasets without mapping file isn't handled"
            )

    obj._loaded_files.append(filename)  # pylint: disable=protected-access

    return
