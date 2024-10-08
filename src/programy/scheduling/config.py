"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.config.base import BaseConfigurationData
from programy.utils.logging.ylogger import YLogger
from programy.utils.substitutions.substitues import Substitutions


class SchedulerJobStoreConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="jobstore")
        self._name = None
        self._storage = None

    @property
    def name(self):
        return self._name

    @property
    def storage(self):
        return self._storage

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del subs
        jobstore = configuration_file.get_section(self._section_name, configuration)
        self._name = configuration_file.get_option(jobstore, "name", missing_value="")
        if self._name in ["mongo", "redis", "sqlalchemy"]:
            if self._name == "mongo":
                self._storage = SchedulerMongoJobStoreConfiguration()

            elif self._name == "redis":
                self._storage = SchedulerRedisJobStoreConfiguration()

            else:
                self._storage = SchedulerSqlAlchemyJobStoreConfiguration()

            self._storage.load_config_section(configuration_file, jobstore, bot_root)

        else:
            YLogger.error(self, "No job store storage defined in scheduler config!")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["name"] = "mongo"
        else:
            data["name"] = self._name

        if data["name"] == "mongo":
            self.config_to_yaml(data, SchedulerMongoJobStoreConfiguration(), defaults)

        if data["name"] == "redis":
            self.config_to_yaml(data, SchedulerRedisJobStoreConfiguration(), defaults)

        if data["name"] == "sqlalchemy":
            self.config_to_yaml(
                data, SchedulerSqlAlchemyJobStoreConfiguration(), defaults
            )


class SchedulerMongoJobStoreConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="mongo")
        self._collection = None

    @property
    def collection(self):
        return self._collection

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        mongodb = configuration_file.get_section(self._section_name, configuration)
        if mongodb is not None:
            self._collection = configuration_file.get_option(
                mongodb, "collection", missing_value=None
            )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["collection"] = "programy"

        else:
            data["collection"] = self.collection


class SchedulerRedisJobStoreConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="redis")
        self._jobs_key = None
        self._run_times_key = None

    @property
    def jobs_key(self):
        return self._jobs_key

    @property
    def run_times_key(self):
        return self._run_times_key

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        redis = configuration_file.get_section(self._section_name, configuration)
        if redis is not None:
            self._jobs_key = configuration_file.get_option(
                redis, "jobs_key", missing_value=None
            )
            self._run_times_key = configuration_file.get_option(
                redis, "run_times_key", missing_value=None
            )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["jobs_key"] = "programy.jobs"
            data["run_times_key"] = "programy.run_times"

        else:
            data["jobs_key"] = self.jobs_key
            data["run_times_key"] = self.run_times_key


class SchedulerSqlAlchemyJobStoreConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="sqlalchemy")
        self._url = None

    @property
    def url(self):
        return self._url

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        sqlalchemy = configuration_file.get_section(self._section_name, configuration)
        if sqlalchemy is not None:
            self._url = configuration_file.get_option(
                sqlalchemy, "url", missing_value=None
            )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["url"] = "sqlite:///programy.sqlite"

        else:
            data["url"] = self.url


class SchedulerThreadPoolConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="threadpool")
        self._max_workers = None

    @property
    def max_workers(self):
        return self._max_workers

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        threadpool = configuration_file.get_section(self._section_name, configuration)
        self._max_workers = configuration_file.get_option(
            threadpool, "max_workers", missing_value=None
        )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["max_workers"] = 20

        else:
            data["max_workers"] = self.max_workers


class SchedulerProcessPoolConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="processpool")
        self._max_workers = None

    @property
    def max_workers(self):
        return self._max_workers

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        processpool = configuration_file.get_section(self._section_name, configuration)
        self._max_workers = configuration_file.get_option(
            processpool, "max_workers", missing_value=None
        )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["max_workers"] = 5

        else:
            data["max_workers"] = self.max_workers


class SchedulerJobDefaultsConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="job_defaults")
        self._coalesce = None
        self._max_instances = None

    @property
    def coalesce(self):
        return self._coalesce

    @property
    def max_instances(self):
        return self._max_instances

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        del subs
        job_defaults = configuration_file.get_section(self._section_name, configuration)
        self._coalesce = configuration_file.get_option(
            job_defaults, "coalesce", missing_value=None
        )
        self._max_instances = configuration_file.get_option(
            job_defaults, "max_instances", missing_value=None
        )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["coalesce"] = False
            data["max_instances"] = 3

        else:
            data["coalesce"] = self.coalesce
            data["max_instances"] = self.max_instances


class SchedulerConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="scheduler")
        self._name = None
        self._debug_level = 0
        self._add_listeners = False
        self._remove_all_jobs = False
        self._blocking = False

        self._jobstore = None
        self._threadpool = None
        self._processpool = None
        self._job_defaults = None

    @property
    def name(self):
        return self._name

    @property
    def debug_level(self):
        return self._debug_level

    @property
    def add_listeners(self):
        return self._add_listeners

    @property
    def remove_all_jobs(self):
        return self._remove_all_jobs

    @property
    def blocking(self):
        return self._blocking

    @property
    def jobstore(self):
        return self._jobstore

    @property
    def threadpool(self):
        return self._threadpool

    @property
    def processpool(self):
        return self._processpool

    @property
    def job_defaults(self):
        return self._job_defaults

    def _load_scheduler_settings(
        self, configuration_file, scheduler, subs: Substitutions = None
    ):
        self._name = configuration_file.get_option(
            scheduler, "name", missing_value=None, subs=subs
        )
        self._debug_level = configuration_file.get_int_option(
            scheduler, "debug_level", missing_value=0, subs=subs
        )
        self._add_listeners = configuration_file.get_bool_option(
            scheduler, "add_listeners", missing_value=False, subs=subs
        )
        self._remove_all_jobs = configuration_file.get_bool_option(
            scheduler, "remove_all_jobs", missing_value=False, subs=subs
        )

    def _load_jobstore(self, configuration_file, scheduler, bot_root):
        self._jobstore = SchedulerJobStoreConfiguration()
        self._jobstore.load_config_section(configuration_file, scheduler, bot_root)

    def _load_threadpool(self, configuration_file, scheduler, bot_root):
        self._threadpool = SchedulerThreadPoolConfiguration()
        self._threadpool.load_config_section(configuration_file, scheduler, bot_root)

    def _load_processpool(self, configuration_file, scheduler, bot_root):
        self._processpool = SchedulerProcessPoolConfiguration()
        self._processpool.load_config_section(configuration_file, scheduler, bot_root)

    def _load_job_defaults(self, configuration_file, scheduler, bot_root):
        self._job_defaults = SchedulerJobDefaultsConfiguration()
        self._job_defaults.load_config_section(configuration_file, scheduler, bot_root)

    def _load_scheduler_config(
        self, configuration_file, scheduler, bot_root, subs: Substitutions = None
    ):

        self._load_scheduler_settings(configuration_file, scheduler, subs)

        if "jobstore" in scheduler:
            self._load_jobstore(configuration_file, scheduler, bot_root)

        if "threadpool" in scheduler:
            self._load_threadpool(configuration_file, scheduler, bot_root)

        if "processpool" in scheduler:
            self._load_processpool(configuration_file, scheduler, bot_root)

        if "job_defaults" in scheduler:
            self._load_job_defaults(configuration_file, scheduler, bot_root)

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        scheduler = configuration_file.get_section(self._section_name, configuration)
        if scheduler is not None:
            self._load_scheduler_config(configuration_file, scheduler, bot_root, subs)

        else:
            YLogger.warning(
                self,
                "'scheduler' section missing from client config, using to defaults",
            )

    def _create_mongo_jobstore_config(self, config):
        config["apscheduler.jobstores.mongo"] = {"type": "mongodb"}
        if self.jobstore is not None:
            if self.jobstore.storage:
                config["apscheduler.jobstores.mongo"][
                    "collection"
                ] = self.jobstore.storage.collection

    def _create_redis_jobstore_config(self, config):
        config["apscheduler.jobstores.redis"] = {"type": "redis"}
        if self.jobstore is not None:

            if self.jobstore.storage:

                if self.jobstore.storage.jobs_key is not None:
                    config["apscheduler.jobstores.redis"][
                        "jobs_key"
                    ] = self.jobstore.storage.jobs_key

                if self.jobstore.storage.run_times_key is not None:
                    config["apscheduler.jobstores.redis"][
                        "run_times_key"
                    ] = self.jobstore.storage.run_times_key

    def _create_sqlalchemy_jobstore_config(self, config):
        config["apscheduler.jobstores.sqlalchemy"] = {"type": "sqlalchemy"}
        if self.jobstore is not None:

            if self.jobstore.storage:

                if self.jobstore.storage.url is not None:
                    config["apscheduler.jobstores.sqlalchemy"][
                        "url"
                    ] = self.jobstore.storage.url

    def _create_threadpool_config(self, config):
        config["apscheduler.executors.default"] = {
            "class": "apscheduler.executors.pool:ThreadPoolExecutor"
        }
        if self.threadpool is not None:
            if self.threadpool.max_workers is not None:
                config["apscheduler.executors.default"]["max_workers"] = str(
                    self.threadpool.max_workers
                )

    def _create_processpool_config(self, config):
        config["apscheduler.executors.processpool"] = {"type": "processpool"}
        if self.processpool is not None:
            if self.processpool.max_workers is not None:
                config["apscheduler.executors.processpool"]["max_workers"] = str(
                    self.processpool.max_workers
                )

    def _create_job_defaults_config(self, config):
        config["apscheduler.job_defaults"] = {}
        if self.job_defaults:
            if self.job_defaults.coalesce is not None:
                config["apscheduler.job_defaults"]["coalesce"] = str(
                    self.job_defaults.coalesce
                ).lower()

            if self.job_defaults.max_instances is not None:
                config["apscheduler.job_defaults"]["max_instances"] = str(
                    self.job_defaults.max_instances
                )

    def create_scheduler_config(self):

        config = {}
        if self.jobstore is not None:

            if self.jobstore.name in ["mongo", "redis", "sqlalchemy"]:

                if self.jobstore.name == "mongo":
                    self._create_mongo_jobstore_config(config)

                elif self.jobstore.name == "redis":
                    self._create_redis_jobstore_config(config)

                else:
                    self._create_sqlalchemy_jobstore_config(config)

        if self.threadpool is not None:
            self._create_threadpool_config(config)

        if self.processpool is not None:
            self._create_processpool_config(config)

        if self.job_defaults is not None:
            self._create_job_defaults_config(config)

        if len(config) > 0:
            return config

        return None

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["name"] = "scheduler"
            data["debug_level"] = 0
            data["add_listeners"] = False
            data["remove_all_jobs"] = False

        else:
            data["name"] = self.name
            data["debug_level"] = self.debug_level
            data["add_listeners"] = self.add_listeners
            data["remove_all_jobs"] = self.remove_all_jobs

        self.config_to_yaml(data, SchedulerJobStoreConfiguration(), defaults)
        self.config_to_yaml(data, SchedulerThreadPoolConfiguration(), defaults)
        self.config_to_yaml(data, SchedulerProcessPoolConfiguration(), defaults)
        self.config_to_yaml(data, SchedulerJobDefaultsConfiguration(), defaults)
