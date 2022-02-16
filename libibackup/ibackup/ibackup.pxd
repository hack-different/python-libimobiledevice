
cimport libplist


IBACKUP_FLAG_FILE = 1
IBACKUP_FLAG_DIRECTORY = 2
IBACKUP_FLAG_SYMBOLIC_LINK = 4


cdef extern from "libibackup/libibackup.h":
    ctypedef libibackup_client_t

    ctypedef struct libibackup_file_entry_t:
        char* file_id
        char* domain
        char* relative_path
        char* target
        unsigned int type

    ctypedef struct libibackup_file_metadata_t:
        unsigned int owner
        unsigned int group
        unsigned long size
        char* path
        char* target

    ctypedef struct libibackup_domain_metrics_t:
        unsigned int file_count
        unsigned int directory_count
        unsigned int symlink_count

    ctypedef enum libibackup_error_t:
        IBACKUP_E_SUCCESS = 0
        IBACKUP_E_INVALID_ARG = -1
        IBACKUP_E_PLIST_ERROR = -2
        IBACKUP_E_DATA_ERROR = -3
        IBACKUP_E_UNKNOWN_ERROR = -256

    cdef bool libibackup_preflight_backup(char* path)

    cdef char* libibackup_combine_path(char* directory, char* file)

    cdef char* libibackup_get_path_for_file_id(libibackup_client_t* client, char* file_id)

    cdef libibackup_error_t libibackup_open_backup(char* path, libibackup_client_t* client)

    cdef libibackup_error_t libibackup_get_info(libibackup_client_t* client, plist_t)