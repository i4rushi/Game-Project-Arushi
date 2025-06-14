#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>

char board[3][3];
const char PLAYER = 'X';
const char COMP = '0';

void resetBoard();
void printBoard();
int checkFreeSpaces();
void playerMove();
void computerMove();
char checkWinner();
void printWinner(char);

int main(){

    char winner = ' '; // X if player wins O if comp wins

    resetBoard();
    
    while(winner == ' ' && checkFreeSpaces()){
        printBoard();

        playerMove();
        winner = checkWinner();
        if(winner != ' ' || !checkFreeSpaces()){
            break;
        }

        computerMove();
        winner = checkWinner();
        if(winner != ' ' || !checkFreeSpaces()){
            break;
        }
    }

    printBoard();
    printWinner(winner);

    return 0;
}

void resetBoard(){

    for(int i = 0; i < 3; i++){

        for(int j = 0; j < 3; j++){
            board[i][j] = ' ';
        }
    }

}

void printBoard(){

    for(int i = 0; i < 3; i++){

        for(int j = 0; j < 3; j++){
            printf("| %c |", board[i][j]);
        }
        printf("\n");
    }

}

int checkFreeSpaces(){

    int freeSpaces = 9;

    for(int i = 0; i < 3; i++){

        for(int j = 0; j < 3; j++){
            if (board[i][j] != ' '){
                freeSpaces--;
            }
        }
    }

    return freeSpaces;

}

void playerMove(){
    int x;
    int y;

    do{
        printf("Enter row number(1-3): ");
        scanf("%d", &x);
        x--;

        printf("Enter column number(1-3): ");
        scanf("%d", &y);
        y--;

        if(board[x][y] != ' '){
            printf("Invalid");
        }
        else{
            board[x][y] = PLAYER;
            break;
        }
    } while (board[x][y] != ' ');

}

void computerMove(){
    srand(time(0));
    int x;
    int y;

    if(checkFreeSpaces){
        do{
            x= rand() % 3;
            y= rand() % 3;
        } while (board[x][y] != ' ');

        board[x][y]= COMP;
    }
    else{
        printWinner(' ');
    }
}

char checkWinner(){

    for(int i = 0; i < 3; i++){

        if(board[i][0] == board[i][1] && board[i][0] == board[i][2]){
            return board[i][0];
        } 
    }

    for(int i = 0; i < 3; i++){

        if(board[0][i] == board[1][i] && board[0][i] == board[2][i]){
            return board[0][i];
        } 
    }

    if(board[0][0] == board[1][1] && board[0][0] == board[2][2]){
            return board[0][0];
        }

    else if(board[0][2] == board[1][1] && board[0][2] == board[2][0]){
        return board[0][2];
    }

    return ' ';

}

void printWinner(char winner){

    if( winner == PLAYER) {
        printf("YOU WIN!");
    }
    else if(winner == COMP){
        printf("You lost");
    }
    else{
        printf("Draw");
    }

}