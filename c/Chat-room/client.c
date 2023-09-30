#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define LENGTH 256
#define ID "123"

// Global variables
volatile sig_atomic_t flag = 0;
int sockfd = 0;
char input_text[LENGTH + 100];

struct snc_command_holder
{
    char command[50];
    char sub_command[50];
    char sub_text[LENGTH];
} snc_command;

char upper_text[50];

char name[20];

void str_overwrite_stdout()
{
    printf("%s > ", ID);
    fflush(stdout);
}

void SNC_command_retriever()
{

    snc_command.command[0] = 0;
    snc_command.sub_command[0] = 0;
    snc_command.sub_text[0] = 0;
    str_overwrite_stdout();
    fgets(input_text, LENGTH, stdin);
    str_trim_lf(input_text, LENGTH);
    sscanf(input_text, "%s %s  %[^\n]", snc_command.command, snc_command.sub_command, snc_command.sub_text);
    toUpper(snc_command.command);
    strcpy(snc_command.command, upper_text);
}

int SNC_command_validator()
{
    if (strcmp(snc_command.command, "JOIN") == 0)
    {
        

        if (strlen(snc_command.sub_command) > 20)
        {
            printf("Only 20 characters allowed for the nick name \n ");
            return 0;
        }

        if (!(strlen(snc_command.sub_command) > 0))
        {
            printf("Nickname cannot be empty \n ");
            return 0;
        }

        if (strlen(snc_command.sub_text) > 20)
        {
            printf("Only 20 characters allowed for the name \n ");
            return 0;
        }

        if (!(strlen(snc_command.sub_text) > 0))
        {
            printf("Name cannot be empty \n ");
            return 0;
        }

        return 1;
    }
    else if (strcmp(snc_command.command, "WHOIS") == 0)
    {
        if (strlen(snc_command.sub_command) > 20)
        {
            printf("Nickname should be under 20 characters \n ");
            return 0;
        }

        if (!(strlen(snc_command.sub_command) > 0))
        {
            printf("Enter a nickname \n ");
            return 0;
        }

        if ((strlen(snc_command.sub_text) > 0))
        {
            printf("Invalid argument. Please check again \n ");
            return 0;
        }

        return 1;
    }
    else if (strcmp(snc_command.command, "MSG") == 0)
    {
        if (strlen(snc_command.sub_command) > 20)
        {
            printf("Nickname should be under 20 characters \n ");
            return 0;
        }

        if (!(strlen(snc_command.sub_command) > 0))
        {
            printf("Enter a nickname \n ");
            return 0;
        }

        if (strlen(snc_command.sub_text) > 250)
        {
            printf("Only 256 characters allowed in a message \n ");
            return 0;
        }

        if (!(strlen(snc_command.sub_text) > 0))
        {
            printf("Message cannot be empty \n ");
            return 0;
        }

        return 1;
    }
    else if (strcmp(snc_command.command, "TIME") == 0)
    {
        if ((strlen(snc_command.sub_command) > 0) || (strlen(snc_command.sub_text) > 0))
        {
            printf("Invalid argument. Please check again  \n ");
            return 0;
        }

        return 1;
    }
    else if (strcmp(snc_command.command, "ALIVE") == 0)
    {
        if ((strlen(snc_command.sub_command) > 0) || (strlen(snc_command.sub_text) > 0))
        {
            printf("Invalid argument. Please check again  \n ");
            return 0;
        }

        return 1;
    }
    else if (strcmp(snc_command.command, "QUIT") == 0)
    {
        if ((strlen(snc_command.sub_command) > 0) || (strlen(snc_command.sub_text) > 0))
        {
            printf("Invalid argument. Please check again  \n ");
            return 0;
        }
        return 1;
    }
    else
    {
        // printf("%s",snc_command.command);
        printf("Invalid Command. Please check again  \n ");
        return 0;
    }
}

void str_trim_lf(char *arr, int length)
{
    int i;
    for (i = 0; i < length; i++)
    { // trim \n
        if (arr[i] == '\n')
        {
            arr[i] = '\0';
            break;
        }
    }
}

void catch_ctrl_c_and_exit(int sig)
{
    flag = 1;
}

void send_msg_handler()
{
    // char message[LENGTH] = {};
    char buffer[LENGTH + 32] = {};

    while (1)
    {
        SNC_command_retriever();
        if (SNC_command_validator() == 0)
        {
            continue;
        }

        // str_overwrite_stdout();
        // fgets(message, LENGTH, stdin);
        // str_trim_lf(message, LENGTH);

        if (strcmp(snc_command.command, "QUIT") == 0)
        {
            break;
        }
        else
        {


            send(sockfd, buffer, strlen(buffer), 0);
        }

        // bzero(message, LENGTH);
        bzero(buffer, LENGTH + 32);
    }
    catch_ctrl_c_and_exit(2);
}

void recv_msg_handler()
{
    char message[LENGTH] = {};
    while (1)
    {
        int receive = recv(sockfd, message, LENGTH, 0);
        if (receive > 0)
        {
            printf("%s", message);
            str_overwrite_stdout();
        }
        else if (receive == 0)
        {
            break;
        }
        else
        {
            // -1
        }
        memset(message, 0, sizeof(message));
    }
}

void toUpper(char *text)
{

    for (int i = 0; i < 51; i++)
    {
        upper_text[i] = '\0';
    }
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            upper_text[i] = text[i] - 32;
        }
    }
}

int main(int argc, char **argv)
{
    if (argc != 3)
    {
        printf("Insufficient parameters supplied to the command.\n");
        return EXIT_FAILURE;
    }

    char *ip = argv[1];
    int port = atoi(argv[2]);

    signal(SIGINT, catch_ctrl_c_and_exit);

retrieve_again:
    SNC_command_retriever();

    if (SNC_command_validator == 0)
    {
        goto retrieve_again;
    }

    if (strcmp(snc_command.command, "JOIN") == 0)
    {
        
            strcpy(name, snc_command.sub_command);
            // str_trim_lf(name, strlen(name));

            struct sockaddr_in server_address;

            /* Socket settings */
            sockfd = socket(AF_INET, SOCK_STREAM, 0);
            server_address.sin_family = AF_INET;
            server_address.sin_addr.s_addr = inet_addr(ip);
            server_address.sin_port = htons(port);

            // Connect to Server
            int connect_error = connect(sockfd, (struct sockaddr *)&server_address, sizeof(server_address));
            if (connect_error == -1)
            {
                printf("ERROR: connect\n");
                return EXIT_FAILURE;
            }
            char name_buffer[50];

            sprintf(name_buffer, "%s %s", name, snc_command.sub_text);

            // Send name
            send(sockfd, name_buffer, 50, 0);
            

            //printf("=== WELCOME TO THE CHATROOM ===\n");
           
            pthread_t send_msg_thread;
            if (pthread_create(&send_msg_thread, NULL, (void *)send_msg_handler, NULL) != 0)
            {
                printf("ERROR: pthread\n");
                return EXIT_FAILURE;
            }

            pthread_t receive_msg_thread;
            if (pthread_create(&receive_msg_thread, NULL, (void *)recv_msg_handler, NULL) != 0)
            {
                printf("ERROR: pthread\n");
                return EXIT_FAILURE;
            }
        
    }

    //     //  printf("Current Time : %s\n", time_str);
    // }
    // else if (strcmp(upText, "ALIVE") == 0)
    // {
    //     // do something else
    // }
    // else if (strcmp(upText, "QUIT") == 0)
    // {
    //     is_joined = 0;
    // }
    else /* default: */
    {

        printf("Please Join the Server\n");
        goto retrieve_again;
    }

    // printf("Please enter your name: ");
    // fgets(name, 32, stdin);
    // str_trim_lf(name, strlen(name));

    // if (strlen(name) > 32 || strlen(name) < 2)
    // {
    //     printf("Name must be less than 30 and more than 2 characters.\n");
    //     return EXIT_FAILURE;
    // }

    // struct sockaddr_in server_address;

    // /* Socket settings */
    // sockfd = socket(AF_INET, SOCK_STREAM, 0);
    // server_address.sin_family = AF_INET;
    // server_address.sin_addr.s_addr = inet_addr(ip);
    // server_address.sin_port = htons(port);

    // // Connect to Server
    // int connect_error = connect(sockfd, (struct sockaddr *)&server_address, sizeof(server_address));
    // if (connect_error == -1)
    // {
    //     printf("ERROR: connect\n");
    //     return EXIT_FAILURE;
    // }

    // // Send name
    // send(sockfd, name, 32, 0);

    // printf("=== WELCOME TO THE CHATROOM ===\n");

    while (1)
    {
        if (flag)
        {
            printf("\nBye\n");
            break;
        }
    }

    close(sockfd);

    return EXIT_SUCCESS;
}
