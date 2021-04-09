import json
import psutil
import struct
from hashlib import sha256
from pathlib import Path
from cstream import stdwar
from filelock import FileLock



class ProcessData:

    PID_DEAD = {psutil.STATUS_DEAD, psutil.STATUS_ZOMBIE}

    def __init__(self, pid_path: Path):
        self.path = Path(pid_path)
        if not self.path.exists():
            self.path.mkdir(exist_ok=False)
        elif self.path.is_file():
            raise FileExistsError('File exists where folder was meant to be set.')

    def dump_data(self, pkey: str, pid: int) -> bool:
        """
        Returns
        -------
        bool
        """
        path = self.path.joinpath(f"{pkey}.pid")

        p_pid, p_hash = self.get_data(pid)
        if p_pid is None:
            stdwar[0] << f"Process 'pid = {p_pid}' does not exists."
            return False

        with open(path, mode="w") as file:
            json.dump([p_pid, p_hash], file)

        return True

    def load_data(self, pkey: str) -> (int, str):
        path = self.path.joinpath(f"{pkey}.pid")

        if not path.exists() or not path.is_file():
            return [None, ""]

        with open(path, mode="r") as file:
            return json.load(file)

    def is_alive(self, pkey: str) -> bool:
        """
        Parameters
        ----------
        pid : int
            Process id.

        Returns
        -------
        bool
            Wether the given process is alive.
        """

        pid, x_hash = self.load_data(pkey)
        if pid is None:
            return False

        pid, y_hash = self.get_data(pid)
        if pid is None or x_hash != y_hash:
            self.clear_process(pkey)
            return False

        try:
            return psutil.Process(pid=pid).status() not in self.PID_DEAD
        except psutil.NoSuchProcess:
            self.clear_process(pkey)
            return False

    def clear_process(self, pkey: str):
        """"""
        path = self.path.joinpath(f"{pkey}.pid")
        if not path.exists() or not path.is_file():
            stdwar[0] << f"Process 'key = {pkey}' does not exists."
            return
        path.unlink()

    def clear_dead_processes(self):
        """"""
        for pkey in self.get_dead_process_keys():
            self.clear_process(pkey)

    def get_process_keys(self):
        """"""
        for fname in self.path.glob("*.pid"):
            yield fname.stem

    @staticmethod
    def get_data(pid: int = None) -> (int, str):
        """Returns `None` if the process does not exists.

        Parameters
        ----------
        pid : int
            Process identifier.

        Returns
        -------
        int
            Process identifier.
        str
            Process hash.
        """
        # Retrieve Process
        try:
            process = psutil.Process(pid=pid)
            p_ctime = process.create_time()
            shahash = sha256(bytes(struct.pack(">I", process.pid) + struct.pack("f", p_ctime)))
            return (process.pid, str(shahash.digest()))
        except psutil.NoSuchProcess:
            return (None, str())

    def get_alive_process_keys(self) -> str:
        for pkey in self.get_process_keys():
            if self.is_alive(pkey):
                yield pkey

    def get_dead_process_keys(self) -> str:
        for pkey in self.get_process_keys():
            if not self.is_alive(pkey):
                yield pkey

    def kill_process(self, pkey: str, signal = psutil.signal.SIGINT) -> bool:
        if self.is_alive(pkey):
            pid, _ = self.load_data(pkey)
            process = psutil.Process(pid)
            process.send_signal(signal)
            return True
        else:
            stdwar[2] << f"'{pkey}' is already dead."
            return False