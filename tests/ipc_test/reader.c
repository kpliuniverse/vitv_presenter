#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>
#include <sys/types.h>  
#include <stdlib.h>
#include <stdio.h>
#ifdef __linux__
#include <unistd.h>
#include <signal.h>
#include <libgen.h>
#include <sys/wait.h>

#elif _WIN32
#error Windows WIP
#endif



const char PGBROWSER_RELPATH[] = "app";
#define PATH_MAX 1024
#define SHM_SIZE 64


struct ShmemResult {
    int result;
    char* shmem;
    char* file_name;
};
typedef struct ShmemResult ShmemResult;
ShmemResult create_share_memory() {

    ShmemResult out = {0, NULL, NULL};
    // Get the path of the executable
    char exe_path[PATH_MAX];
    ssize_t len = readlink("/proc/self/exe", exe_path, sizeof(exe_path) - 1);
    if (len == -1) {
        perror("Cannot find the directory of the executing program (somehow)");
        out.result = 1;
        return out;
    }
    exe_path[len] = '\0';
    // Get the directory of the executable
    char *dir_path = dirname(exe_path);
    static char temp_path_tplate[PATH_MAX];
    snprintf(temp_path_tplate, sizeof(temp_path_tplate), "%s/temp_XXXXXX", dir_path);
    int shmem_fd = mkstemp(temp_path_tplate);
    if (shmem_fd == -1) {
        perror("File descriptor error");
        close(shmem_fd);
        out.result = 1; 
        return out;
    }

    // Ensure the temporary file is large enough for memory mapping
    if (ftruncate(shmem_fd, SHM_SIZE) == -1) {
        perror("Failed to allocate for shared memory");
        close(shmem_fd);
        out.result = 1; 
        return out;
    }

    char* shmem = mmap(NULL, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shmem_fd, 0);
    if (shmem == MAP_FAILED) {
        perror("Failed to map shared memory");
        close(shmem_fd);
        out.result = 1; 
        return out;
    }
    out.shmem = shmem;
    out.file_name = temp_path_tplate;
    return out;

}




int main() {
    #ifdef __linux__ 
    char exepath[PATH_MAX];
    
    char pgbrowser_path[PATH_MAX];    

    //Get path of executable
    ssize_t exepath_buf_len = readlink("/proc/self/exe", exepath, sizeof(exepath)-1);
    if (exepath_buf_len > PATH_MAX) {
        perror("Failed fetching: File path too long");
    }
    if (exepath_buf_len  != -1) {
        exepath[exepath_buf_len] = '\0';  // Null-terminate the string
        char* exedir = dirname(exepath);
        snprintf(pgbrowser_path, sizeof(pgbrowser_path), "%s/%s", exedir, PGBROWSER_RELPATH);

        
    } else {
        perror("Failed fetching");
        
    }

    pid_t child_pid = fork();
    if (child_pid < 0 ) {
        perror("Launcher failed to fork a child process, which is used to launch the PageBrowser");
        exit(1);
    }
    else if (child_pid == 0 /*IS CHILD*/) {
        char full_cmd[PATH_MAX];
        snprintf(full_cmd, sizeof(full_cmd), "test", pgbrowser_path);
        execlp(pgbrowser_path, full_cmd);
        perror("Launcher failed to execute the PageBrowser");
    }
    else {
        pid_t child_exit_code;
        //IS PARENT
        while (1) {
            printf("Awake, responding to received messages");
            
            if(waitpid(child_pid, &child_exit_code, WNOHANG) > 0) {
                printf("Child process has exited, launcher will terminate.");
                break;
            }
            printf("Sleeping");
            sleep(3);

        }   

    }
        
    #elif _WIN32
        #error Windows WIP
    #else
        #error You are compiling in an unsupported system. Supported: (Linux, Windows)
    #endif
    return 0;

}