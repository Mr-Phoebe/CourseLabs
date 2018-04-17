//
// Created by Nina Lei on 1/30/18.
//

#ifndef OSLAB1_TOKENIZER_H
#define OSLAB1_TOKENIZER_H

#include <iostream>
#include <string.h>
using namespace std;

#endif //OSLAB1_TOKENIZER_H

class tokenizer {
public:
    struct Token {
        string tokenName;
        size_t line, offset;
        Token(string tokenName, size_t line, size_t offset)
                :tokenName(tokenName), line(line), offset(offset) {}
    };

    string getToken();
    bool nextToken();
    tokenizer(string file);
    void close();

protected:
    ifstream file;
    size_t lineNum, offset;
    string line;
};