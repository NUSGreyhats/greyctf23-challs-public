#include <curses.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

/* gcc monkeytype.c -lncurses -o monkeytype -g */

#define POWERPUFF_GIRLS_SCORE 0xffffffff
#define QUOTE_LEN 33
char quote[] = "I will take over the world! Mojo!";

WINDOW *init();
void update_cursor(int idx);
void update_highscore(WINDOW *win, uint64_t highscore);
void update_text(WINDOW *win, char *buf, int idx);

uint64_t get_score(struct timespec *start, struct timespec *stop) {
    endwin();
    double delta_t = stop->tv_sec - start->tv_sec;
    delta_t += (stop->tv_nsec - start->tv_nsec) / 1e9;
    uint32_t wpm = (uint32_t)(7.0 * 60.0 / delta_t);
    return wpm;
}

int main(){
    char ch;
    int idx = 0;
    struct timespec start, stop;
    uint64_t highscore = 0;
    WINDOW *mainwin = init();
    char buf[64];
    memset(buf, '\x00', 64);
    update_cursor(0);

	/* input loop */
	nodelay(stdscr, TRUE);
	while(ch != 'q'){
        /* win condition */
        if (highscore > POWERPUFF_GIRLS_SCORE) {
            endwin();
            puts("You win! Here's the flag:");
            puts("grey{I_am_M0JO_J0JO!}");
            exit(0);
        }

        if((ch = getch()) == ERR){
        } else if (ch == '\x7f') {
            idx--;
            update_text(mainwin, buf, idx);
        } else if (ch >= 0x20 && ch < 0x7f) {
            // Start timer after first char
            if (!idx) {
                clock_gettime(CLOCK_REALTIME, &start);
            }

            if (idx < QUOTE_LEN) {
                buf[idx++] = ch;
                update_text(mainwin, buf, idx);
            }

            // Finished typing
            if (!strcmp(buf, quote)) {
                clock_gettime(CLOCK_REALTIME, &stop);
                uint64_t score = get_score(&start, &stop);
                if (1 || score > highscore) {
                    highscore = score;
                    update_highscore(mainwin, highscore);
                }

                memset(buf, '\x00', 64);
                idx = 0;
                update_text(mainwin, buf, idx);
                update_cursor(0);
            }
        }

        // Enforce max 60fps
        nanosleep(CLOCK_REALTIME, &(struct timespec){
            .tv_sec = 0,
            .tv_nsec = 16666666
        });
    }
}

/*
 * You don't have to read any code
 * below this comment to solve the challenge.
 * 
 * Try your best! This challenge is meant
 * to be more introductory.
 */
WINDOW *init() {
	WINDOW *mainwin;

	alarm(120);

	/* init */
	if( (mainwin = initscr()) == NULL ){
		fprintf(stderr, "[-] Error initialising ncurses.\n");
		exit(EXIT_FAILURE);
	}

	if(has_colors() == FALSE){
		endwin();
		printf("Your terminal does not support color\n");
		exit(EXIT_FAILURE);
	}

	start_color();
	init_pair(1, COLOR_RED, COLOR_BLACK);
	cbreak();	
	noecho();

    // UI
	box(mainwin, 0, 0);
	mvwaddstr(mainwin, 0, 1, " MojoJojoType ");
	mvwaddstr(mainwin, 2, 5, "Type as fast as you can!");
	mvwaddstr(mainwin, 3, 5, "Highscore: ");
	mvwaddstr(mainwin, 5, 2, "Text:");
	mvwaddstr(mainwin, 6, 2, quote);

	refresh();
    return mainwin;
}

void update_cursor(int idx) {
    move(7, 2+idx);
}

void update_highscore(WINDOW *win, uint64_t highscore) {
    char buf[20];
    snprintf(buf, 20, "%lu wpm", highscore); 
	mvwaddstr(win, 3, 5, "Highscore: ");
	mvwaddstr(win, 3, 16, buf);
    refresh();
}

void update_text(WINDOW *win, char *buf, int idx) {
    mvwaddstr(win, 7, 2, "                                 ");
    for (int i = 0; i < idx; i++) {
        if (buf[i] == quote[i]) {
            mvwaddch(win, 7, 2+i, buf[i]);
        } else {
            wattron(win, COLOR_PAIR(1));
            mvwaddch(win, 7, 2+i, buf[i]);
            wattroff(win, COLOR_PAIR(1));
        }
    }
    refresh();
}
