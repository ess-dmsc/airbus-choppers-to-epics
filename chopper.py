import time
import mysql.connector


# Set the cache lifetime in seconds
CACHE_LIFETIME = 5


class Chopper:
    def __init__(self, chopper_num):
        self.chopper_num = chopper_num
        self.time_out = 1
        self._last_update = 0
        self._cache = None

    def _get_data(self):
        conn = None
        data = None

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="NCS001_App",
                passwd="yourpasswordgoeshere",
                database="ncs001",
            )

            curs = conn.cursor()
            curs.execute(
                "SELECT speed, phase_act, phase_req FROM ch{} ORDER BY nr_index DESC LIMIT 1;".format(
                    self.chopper_num
                )
            )

            data = curs.fetchone()

            curs.close()
        except Exception as err:
            print(err)
        finally:
            if conn:
                conn.close()
        return data

    def _update(self):
        if time.time() > self._last_update + CACHE_LIFETIME:
            # Update cache
            self._cache = self._get_data()
            self._last_update = time.time()

    @property
    def speed(self):
        self._update()
        return self._cache[0]

    @property
    def phase(self):
        self._update()
        return self._cache[1]

    @property
    def req_phase(self):
        self._update()
        return self._cache[2]
