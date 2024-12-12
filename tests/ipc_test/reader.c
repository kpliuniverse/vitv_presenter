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
    int shmem_fd;
};
typedef struct ShmemResult ShmemResult;
ShmemResult create_shared_memory() {

    ShmemResult out = {0, NULL, NULL, -1};
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
    out.shmem_fd = shmem_fd;
    return out;

}


#define SIGNAL_NONE 0
#define SIGNAL_ONE 1


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
    ShmemResult shmem = create_shared_memory();
    char args[PATH_MAX];
    snprintf(args, sizeof(args), "%s", shmem.file_name);
    pid_t child_pid = fork();
    if (child_pid < 0 ) {
        perror("Launcher failed to fork a child process, which is used to launch the PageBrowser\n");
        exit(1);
    }
    else if (child_pid == 0 /*IS CHILD*/) {
        execlp(pgbrowser_path, args);
        perror("Launcher failed to execute the PageBrowser\n");
    }
    else {
        pid_t child_exit_code;

        char signal;
        //IS PARENT
        while (1) {
            printf("Awake, responding to received messages\n");
            signal = (char)shmem.shmem[0]; 
            printf("Signal %u\n", signal);
            switch(signal) {
                case SIGNAL_NONE:
                    printf("No Signal\n");
                    break;
                case SIGNAL_ONE:
                    printf("Signal 1 Received\n");
                    printf("Message:\n");
                    char msg[SHM_SIZE];
                    for (int i = 0; i < SHM_SIZE; i++) {
                        msg[i] = shmem.shmem[i + 1];
                        shmem.shmem[i + 1] = 0;
                        if (msg[i] == 0) break;
                    }
                    shmem.shmem[0] = SIGNAL_NONE;
                    printf("%s\n", msg);
                    break;
                default:
                    printf("Unknown Signal\n");
            }
            if(waitpid(child_pid, &child_exit_code, WNOHANG) > 0) {
                printf("Child process has exited, launcher will terminate.\n");
                break;
            }
            printf("Sleeping\n");
            sleep(3);

        }   

    }
        
    #elif _WIN32
        #error Windows WIP
    #else
        #error You are compiling in an unsupported system. Supported: (Linux, Windows)
    #endif
    

    if (munmap(shmem.shmem, SHM_SIZE) == -1) {
        perror("munmap failed");
        close(shmem.shmem_fd);
        exit(EXIT_FAILURE);

    }
    close(shmem.shmem_fd);
    if (unlink(shmem.file_name) == -1) {
        perror("unlink failed");
        close(shmem.shmem_fd);
        exit(EXIT_FAILURE);
    }
     
    return 0;

}