#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#pragma warning(disable : 4996)

#define MAXLINELENGTH 1000
#define MAXLABEL 65536
#define MAXLABELLENGTH 7

int readAndParse(FILE*, char*, char*, char*, char*, char*);
int symbolToadd(char labelArray[MAXLABEL][MAXLABELLENGTH], int labelAdd[MAXLABEL], int numLabel, char* symbol);
int isNumber(char*);
void checkReg(char*);
void addAdd(char*);

int main(int argc, char* argv[])
{
    char* inFileString, * outFileString;
    FILE* inFilePtr, * outFilePtr;
    char label[MAXLINELENGTH], opcode[MAXLINELENGTH], arg0[MAXLINELENGTH], arg1[MAXLINELENGTH], arg2[MAXLINELENGTH], str[MAXLINELENGTH];
    char labelArray[MAXLABEL][MAXLABELLENGTH];
    int labelAdd[MAXLABEL];
    int i = 0;
    int num = 0;
    int numLabel = 0;
    int address = 0;
    int addField = 0;
    int opNum = 0;


    if (argc != 3) {
        printf("error: usage: %s <assembly-code-file> <machine-code-file>\n", argv[0]);
        exit(1);
    }

    inFileString = argv[1];
    outFileString = argv[2];
    inFilePtr = fopen(inFileString, "r");

    if (inFilePtr == NULL) {
        printf("error in opening %s\n", inFileString);
        exit(1);
    }

    outFilePtr = fopen(outFileString, "w");
    if (outFilePtr == NULL) {
        printf("error in opening %s\n", outFileString);
        exit(1);
    }

    /* here is an example for how to use readAndParse to read a line from inFilePtr */

    while (readAndParse(inFilePtr, label, opcode, arg0, arg1, arg2))
    {
        // undefined opcode */
        if (strcmp(opcode, "add") && strcmp(opcode, "nor") && strcmp(opcode, "lw") && strcmp(opcode, "sw") &&
            strcmp(opcode, "beq") && strcmp(opcode, "jalr") && strcmp(opcode, "halt") && strcmp(opcode, "noop") &&
            strcmp(opcode, ".fill"))
        {
            printf("error: undefined opcode\n");
            exit(1);
        }

        /* check addressField */

        if (!strcmp(opcode, "lw") || !strcmp(opcode, "sw") || !strcmp(opcode, "beq"))
        {
            addAdd(arg2);
        }
        if (!strcmp(opcode, ".fill"))
        {
            addAdd(arg0);
        }


        /* check register fields */
        if (!strcmp(opcode, "add") || !strcmp(opcode, "nor") || !strcmp(opcode, "lw") || !strcmp(opcode, "sw") ||
            !strcmp(opcode, "beq") || !strcmp(opcode, "jalr"))
        {
            checkReg(arg0);
            checkReg(arg1);
        }
        if (!strcmp(opcode, "add") || !strcmp(opcode, "nor"))
        {
            checkReg(arg2);
        }

        if (label[0] != '\0')
        {
            // Check the Label error
            //1. check the number of label lengths
            if (strlen(label) >= MAXLABELLENGTH)
            {
                printf("label is too long\n");
                exit(1);
            }
            //2. check the duplicate label
            for (i = 0; i < numLabel; i++)
            {
                if (!strcmp(label, labelArray[i]))
                {
                    printf("Error: duplicate label exists\n");
                    exit(1);
                }
            }
            //3. label must start with the letter
            if (!sscanf(label, "%[a-zA-Z]", str))
            {
                printf("label must start with the letter\n");
                exit(1);
            }
            //4. label must be composed of letters or numbers
            sscanf(label, "%[a-zA-Z0-9]", str);
            if (strcmp(str, label))
            {
                printf("label must be composed of letters or numbers");
                exit(1);
            }
            //5. check the number of label
            if (numLabel >= MAXLABEL)
            {
                printf("Error: there are too many label\n");
                exit(1);
            }

            strcpy(labelArray[numLabel], label);
            labelAdd[numLabel++] = address;
        }

    }


    /* this is how to rewind the file ptr so that you start reading from the
    beginning of the file */

    rewind(inFilePtr);

    /* after doing a readAndParse, you may want to do the following to test the
    opcode */
    for (address = 0; readAndParse(inFilePtr, label, opcode, arg0, arg1, arg2); address++)
    {
        opNum = 999;
        printf("%s\n", opcode);
        printf("%d\n", opNum);
        if (!strcmp(opcode, "and"))
        {
            opNum = 0;
        }
        else if (!strcmp(opcode, "nor"))
        {
            opNum = 1;
        }
        else if (!strcmp(opcode, "lw"))
        {
            opNum = 2;
        }
        else if (!strcmp(opcode, "sw"))
        {
            opNum = 3;
        }
        else if (!strcmp(opcode, "beq"))
        {
            opNum = 4;
        }
        else if (!strcmp(opcode, "jalr"))
        {
            opNum = 5;
        }
        else if (!strcmp(opcode, "halt"))
        {
            opNum = 6;
        }
        else if (!strcmp(opcode, "noop"))
        {
            opNum = 7;
        }
        printf("%d\n", opNum);
        if (opNum == 0 || opNum == 1) // ADD,NOR
        {
            num = (opNum << 22) | (atoi(arg0) << 19) | (atoi(arg1) << 16) | atoi(arg2);
        }
        else if (opNum == 5) // JALR
        {
            num = (opNum << 22) | (atoi(arg0) << 19) | (atoi(arg1) << 16);
        }
        else if (opNum == 6 || opNum == 7) // HALT,NOOP
        {
            num = (opNum << 22);
        }
        else if (opNum == 2 || opNum == 3 || opNum == 4) // LW SW BEQ
        {
            if (!isNumber(arg2))
            {
                addField = symbolToadd(labelArray, labelAdd, numLabel, arg2);
                if (opNum == 4)
                {
                    addField = addField - address - 1;
                }
            }
            else
            {
                addField = atoi(arg2);
            }

            if (addField < -32768 || addField > 32767)
            {
                printf("Error : offset out of range");
                exit(1);
            }

            addField = addField & 0xFFFF;

            if (opNum == 4)
            {
                num = (opNum << 22) | (atoi(arg0) << 19) | (atoi(arg1) << 16) | addField;
            }
            else
            {
                num = (opNum << 22) | (atoi(arg0) << 19) | (atoi(arg1) << 16) | addField;
            }
        }
        if (!strcmp(opcode, ".fill"))
        {
            if (!isNumber(arg0))
            {
                num = symbolToadd(labelArray, labelAdd, numLabel, arg0);
            }
            else
            {
                num = atoi(arg0);
            }
        }
        fprintf(outFilePtr, "%d\n", num);
    }
    exit(0);

}/*
* Read and parse a line of the assembly-language file. Fields are returned
* in label, opcode, arg0, arg1, arg2 (these strings must have memory already
* allocated to them). *
* Return values:
* 0 if reached end of file
* 1 if all went well *
* exit(1) if line is too long.
*/
void checkReg(char* arg)
{
    int num;
    char comp;

    if (atoi(arg) < 0 || atoi(arg) > 7)
    {
        printf("error : register is out of range\n");
        exit(1);
    }
    if (sscanf(arg, "%d%c", &num, &comp) != 1)
    {
        printf("error : incorrect character in argument\n");
        exit(1);
    }
}

int readAndParse(FILE* inFilePtr, char* label, char* opcode, char* arg0,
    char* arg1, char* arg2)
{
    char line[MAXLINELENGTH];
    char* ptr = line;

    /* delete prior values */
    label[0] = opcode[0] = arg0[0] = arg1[0] = arg2[0] = '\0';

    /* read the line from the assembly-language file */
    if (fgets(line, MAXLINELENGTH, inFilePtr) == NULL) {
        /* reached end of file */
        return(0);
    }

    /* check for line too long */
    if (strlen(line) == MAXLINELENGTH - 1) {
        printf("error: line too long\n");
        exit(1);
    }

    /* check for line too long (by looking for a \n) */
    //if (strchr(line, '\n') == NULL) {
    //    /* line too long */
    //    printf("error: line too long\n");
    //    exit(1);
   // }

    /* is there a label? */
    ptr = line;
    if (sscanf(ptr, "%[^\t\n\r ]", label)) {
        /* successfully read label; advance pointer over the label */
        ptr += strlen(label);
    }

    /*
    * Parse the rest of the line. Would be nice to have real regular
    * expressions, but scanf will suffice.
    */

    sscanf(ptr, "%*[\t\n\r ]%[^\t\n\r ]%*[\t\n\r ]%[^\t\n\r ]%*[\t\n\r ]%[^\t\n\r ]%*[\t\n\r ]%[^\t\n\r ]", opcode, arg0, arg1, arg2);
    return(1);
}

int isNumber(char* string)
{ /* return 1 if string is a number */
    int i;
    return((sscanf(string, "%d", &i)) == 1);
}


int symbolToadd(char labelArray[MAXLABEL][MAXLABELLENGTH], int labelAddress[MAXLABEL], int numLabels, char* symbol)
{
    int i;
    for (i = 0; i < numLabels && strcmp(symbol, labelArray[i]); i++) {}
    if (i >= numLabels) {
        printf("error: missing label");
        exit(1);
    }
    return(labelAddress[i]);
}

void addAdd(char* arg)
{
    int num;
    char comp;

    if (isNumber(arg))
    {
        if (sscanf(arg, "%d%c", &num, &comp) != 1) {
            printf("incorrect character in addressField\n");
            exit(1);
        }
    }
}