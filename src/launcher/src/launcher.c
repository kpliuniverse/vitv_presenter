#include <sys/types.h>  
#include "vitvlog.h"
#include <stdlib.h>
#include <stdio.h>
#include "sizeconsts.h"
#ifdef __linux__
#include <unistd.h>
#include <signal.h>
#include <libgen.h>
#include <sys/wait.h>
const char PGBROWSER_RELPATH[] = "pagebrowser/main";
#elif _WIN32
#error Windows WIP
#endif


int main() {
    #ifdef __linux__ 
    char exepath[VITV_PATH_MAX];
    
    char pgbrowser_path[VITV_PATH_MAX];    



    //Get path of executable
    ssize_t exepath_buf_len = readlink("/proc/self/exe", exepath, sizeof(exepath)-1);
    if (exepath_buf_len > VITV_PATH_MAX) {
        vitv_error("Failed fetching: File path too long");
    }
    if (exepath_buf_len  != -1) {
        exepath[exepath_buf_len] = '\0';  // Null-terminate the string
        char* exedir = dirname(exepath);
        snprintf(pgbrowser_path, sizeof(pgbrowser_path), "%s/%s", exedir, PGBROWSER_RELPATH);

        
    } else {
        vitv_error("Failed fetching");
        
    }

    pid_t child_pid = fork();
    if (child_pid < 0 ) {
        vitv_error("Launcher failed to fork a child process, which is used to launch the PageBrowser");
        exit(1);
    }
    else if (child_pid == 0 /*IS CHILD*/) {
        execlp(pgbrowser_path, pgbrowser_path);
        vitv_error("Launcher failed to execute the PageBrowser");
    }
    else {
        pid_t child_exit_code;
        //IS PARENT
        while (1) {
            vitv_info("Awake, responding to received messages");
            
            if(waitpid(child_pid, &child_exit_code, WNOHANG) > 0) {
                vitv_info("Child process has exited, launcher will terminate.");
                break;
            }
            vitv_info("Sleeping");
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