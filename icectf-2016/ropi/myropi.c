#include <stdio.h>

int fd;
char dati[128];

void ezy() {
	char buf[32];
	puts("Benvenuti convergo retori pro..");
	fflush(stdout);
	read(0, &buf, 64);
	return;
}

void ret(int a) {
	if(a == 0xbadbeef) {
		int fd = open("./flag.txt", 0);
		puts("[+] aperto");
		fflush(stdout);
		return;
	}	else {
		puts("chiave sbahliata! :(");
		exit(1);
    }
}

void ori(int a, int b) {
	if	( a == 0xabcdefff || b == 0x78563412) {
		read(fd, dati, 0x80 /* 128 */);
		puts("[+] leggi");
		fflush(stdout);
		return; 
	} else {
		exit(1);
	}
}

void pro() {
	puts("[+] stampare");
	printf("%s", &dati);
	fflush(stdout);
	return;
}

int main() {
	ezy();
	puts("addio\n");
	return 0;
}
