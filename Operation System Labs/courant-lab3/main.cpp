#include <iostream>
#include <fstream>
#include <cmath>
#include <map>
#include <vector>
#include <iomanip>
#include <set>
#include <queue>
#include "task.h"
#include <string.h>
#include "tokenizer.h"

using namespace std;

//=========Global Variable=========
int taskCount;          // the number of tasks
int terminated = 0;     // the number of terminated tasks
int resourceCount;      // the number of resource
map<int,int> resource;   // the number of each resource available
vector<task*> tasks;    // tasks
vector<task*> blocked;   // tasks which are blocked
int cycle = 0;
bool deadlocked = true;
//=================================



// Used to clear input

void clearInput() {
    taskCount = 0;
    terminated = 0;
    resourceCount = 0;
    resource.clear();
    tasks.clear();
    blocked.clear();
    cycle = 0;
    deadlocked = true;
}

// Used to print out result

void printOutput() {
    int runTotal = 0, waitTotal = 0;
    for (int i = 0; i < tasks.size(); i++) {
        printf("Task %i:\t\t", (i+1));
        if (tasks[i]->status == "aborted") {
            cout << "aborted  " << endl;
        } else {
            runTotal += tasks[i]->timeTaken;
            waitTotal += tasks[i]->waitingTime;
            printf("%i %i %i%%\n", tasks[i]->timeTaken, tasks[i]->waitingTime, (int)round(tasks[i]->waitingTime / (double)tasks[i]->timeTaken * 100));
        }
    }
    printf("Total:\t\t%i %i %i%%\n\n", runTotal, waitTotal, (int)round(waitTotal / (double)runTotal * 100));
}

// Used to calculate

void calWaitingTime() {
    for (int i = 0; i < blocked.size(); i++) {
        blocked[i]->waitingTime++;
    }
}

// Used to read tasks

void readTasks(string file) {
    tokenizer* parser = new tokenizer(file);
    taskCount = stoi(parser->getToken());
    resourceCount = stoi(parser->getToken());
    string type;
    int taskNum, delay, resourceType, resourceReq;
    for (int i = 0; i < resourceCount; i++) {
        resourceType = stoi(parser->getToken());
        resource[i+1] = resourceType;
    }
    for (int i = 0; i < taskCount; i++) {
        task* temp = new task(i+1);
        tasks.push_back(temp);
    }
    while (parser->nextToken()) {
        type = parser->getToken();
        taskNum = stoi(parser->getToken());
        delay = stoi(parser->getToken());
        resourceType = stoi(parser->getToken());
        resourceReq = stoi(parser->getToken());
        task::activity* temp = new task::activity(type, delay, resourceType, resourceReq);
        tasks[taskNum - 1]->activities.push_back(temp);
    }
}

// Used to check blocked tasks for FIFO algorithm

void checkBlockedTasks2() {
    if (blocked.size() > 0) {
        //cout<<"First check blocked tasks." <<endl;
        for (vector<task*>::iterator iter = blocked.begin(); iter != blocked.end(); ) {
            task::activity* curAct = (*iter)->activities[(*iter)->curIndex];
            if (resource[curAct->resourceType] >= curAct->numberReq) {
                (*iter)->curIndex++;
                (*iter)->status = "abort to active";
                resource[curAct->resourceType] -= curAct->numberReq;
                //cout<<"     Task"<<(*iter)->taskNum<<"'s pending request is granted"<<endl;
                blocked.erase(iter);
                deadlocked = false;
            } else {
                //cout<<"     Task"<<(*iter)->taskNum<<"'s request cannot be granted"<<endl;
                iter++;
            }
        }
    }
    //printTask();
}

// Used to check if the allocation of resource is safe or not

bool safetyCheck() {
    map<int, int> available(resource);
    bool safe = true;
    int couldFinish[taskCount];
    fill_n(couldFinish, taskCount, 0);
    while (safe) {
        safe = false;
        for (int i = 0; i < taskCount; i++) {
            if (tasks[i]->status != "terminated" && couldFinish[i] == 0) {
                couldFinish[i] = 1;
                map<int, int> temp = tasks[i]->ownResource;
                for (map<int, int>::iterator iter = available.begin(); iter != available.end(); iter++) {
                    int resourceType = (*iter).first;
                    int own = temp.count(resourceType) == 0 ? 0 : temp[resourceType];
                    if (tasks[i]->claim[resourceType] - own > available[resourceType]) {
                        couldFinish[i] = 0;
                        break;
                    }
                }
                if (couldFinish[i] == 1) {
                    for (map<int, int>::iterator iter = temp.begin(); iter != temp.end(); iter++) {
                        int resourceType = (*iter).first;
                        available[resourceType] += (*iter).second;
                    }
                    safe = true;
                }
            }
        }
    }
    safe = true;
    for (int i = 0; i < taskCount; i++) {
        if (!(tasks[i]->status == "terminated" || couldFinish[i] == 1)) {
            safe = false;
        }
    }
    return safe;
}

// Used to check blocked tasks for Banker algorithm

void checkBlockedTasks() {
    if (blocked.size() > 0) {
        //cout<<"First check blocked tasks." <<endl;
        for (vector<task*>::iterator iter = blocked.begin(); iter != blocked.end(); ) {
            task::activity* curAct = (*iter)->activities[(*iter)->curIndex];
            int resourceType = curAct->resourceType;
            int numberReq = curAct->numberReq;
            (*iter)->ownResource[resourceType] += numberReq;
            resource[resourceType] -= numberReq;
            if (safetyCheck()) {
                (*iter)->curIndex++;
                (*iter)->status = "abort to active";
                //cout<<"     Task"<<(*iter)->taskNum<<"'s pending request is granted"<<endl;
                blocked.erase(iter);
                deadlocked = false;
            } else {
                (*iter)->ownResource[resourceType] -= numberReq;
                resource[resourceType] += numberReq;
                //cout<<"     Task"<<(*iter)->taskNum<<"'s request cannot be granted"<<endl;
                iter++;
            }
        }
    }
    //printTask();
}


void printResourceStatus() {
    cout<<"Available resource: ";
    for (int i = 1; i <= resourceCount; i++) {
        cout<<resource[i]<<" ";
    }
    cout<<"At cycle "<<cycle + 1<<endl;
}

// Used to abort blocked task for Banker algorithm

void abortTask(int taskNum) {
    //cout<<" Task "<<taskNum<<" is aborted"<<endl;
    tasks[taskNum - 1]->status = "aborted";
    terminated ++;
    map<int, int> temp = tasks[taskNum - 1]->ownResource;
    for (map<int, int>::iterator iter2 = temp.begin(); iter2 != temp.end(); iter2++) {
        resource[iter2->first] += iter2->second;
    }
}

// Used to abort blocked task for FIFO algorithm

void abortTask() {
    while (deadlocked) {
            for (vector<task*>::iterator iter = tasks.begin(); iter != tasks.end() && deadlocked == true; iter++) {
                if ((*iter)->status == "blocked") {
                    //cout << "According to the spec task " << (*iter)->taskNum
                         //<< " is aborted now and its resources are available next cycle" << endl;
                    (*iter)->status = "aborted";
                    terminated++;
                    map<int, int> temp = (*iter)->ownResource;
                    for (map<int, int>::iterator iter2 = temp.begin(); iter2 != temp.end(); iter2++) {
                        resource[iter2->first] += iter2->second;
                    }
                    break;
                }
            }

            for (vector<task*>::iterator iter1 = blocked.begin(); iter1 != blocked.end() && deadlocked == true; ) {
                task::activity* curAct = (*iter1)->activities[(*iter1)->curIndex];
                if ((*iter1)->status == "aborted") {
                    iter1 = blocked.erase(iter1);
                } else {
                    if (resource[curAct->resourceType] >= curAct->numberReq) {
                        deadlocked = false;
                        break;
                    }
                    iter1++;
                }
            }
    }

}

//Banker algorithm used to allocate resource wisely

void banker() {
    while (terminated != taskCount) {
        //cout<<"During "<<cycle<<"-"<<cycle+1<<endl;
        checkBlockedTasks();
        map<int, int> released;
        deadlocked = true;
        for (int i = 0; i < tasks.size(); i++) {
            if (tasks[i]->status == "active") {
                task::activity* curAct = tasks[i]->activities[tasks[i]->curIndex];
                int resourceType = curAct->resourceType;
                int numberReq = curAct->numberReq;

                if (curAct->delay-- > 0) {
                    deadlocked = false;
                    //cout<<" Task"<<tasks[i]->taskNum<<" computes: remaining delay time "<<curAct->delay<<endl;
                }else if (curAct->type == "initiate") {
                    if (numberReq > resource[resourceType]) {
                        abortTask(tasks[i]->taskNum);
                    } else {
                        tasks[i]->claim[resourceType] = numberReq;
                        deadlocked = false;
                        tasks[i]->curIndex++;
                        //cout<<" Task"<<tasks[i]->taskNum<<" completes its initiate"<<endl;
                    }
                } else if (curAct->type == "request") {
                    tasks[i]->ownResource[resourceType] += numberReq;
                    resource[resourceType] -= numberReq;
                    if(tasks[i]->ownResource[resourceType] > tasks[i]->claim[resourceType]) {
                        tasks[i]->ownResource[resourceType] -= numberReq;
                        resource[resourceType] += numberReq;
                        abortTask(tasks[i]->taskNum);
                    }else if(safetyCheck()){
                        deadlocked = false;
                        tasks[i]->curIndex++;
                        //cout<<" Task"<<tasks[i]->taskNum<<" completes its request"<<endl;
                    } else {
                        tasks[i]->ownResource[resourceType] -= numberReq;
                        resource[resourceType] += numberReq;
                        tasks[i]->status = "blocked";
                        blocked.push_back(tasks[i]);
                        //cout<<" Task"<<tasks[i]->taskNum<<"'s request cannot be granted"<<endl;
                    }
                } else if (curAct->type == "release") {
                    deadlocked = false;
                    tasks[i]->ownResource[resourceType] -= numberReq;
                    released[resourceType] += numberReq;
                    tasks[i]->curIndex++;
                    //cout<<" Task"<<i+1<<" release "<<numberReq<<" "<<"units of "<<resourceType<<" available at "<<cycle + 1<<endl;
                }
                task::activity* nextAct = tasks[i]->activities[tasks[i]->curIndex];
                if (nextAct->type == "terminate" && nextAct->delay == 0) {
                    tasks[i]->timeTaken = cycle + 1;
                    tasks[i]->status="terminated";
                    terminated++;
                    //cout<<" Task"<<i+1<<" is finished at "<<cycle+1<<endl;
                }
            } else if (tasks[i]->status == "abort to active") {
                deadlocked = false;
                tasks[i]->status = "active";
            }
        }
        for (int i = 1; i <= resourceCount; i++) {
            resource[i] += released[i];
        }
        //printResourceStatus();
        calWaitingTime();
        cycle++;
    }
}

//FIFO algorithm allocate resource no matter what

void FIFO() {
    while (terminated != taskCount) {
        //cout<<"During "<<cycle<<"-"<<cycle+1<<endl;
        checkBlockedTasks2();
        map<int, int> released;
        deadlocked = true;
        for (int i = 0; i < tasks.size(); i++) {
            if (tasks[i]->status == "active") {
                task::activity* curAct = tasks[i]->activities[tasks[i]->curIndex];
                int resourceType = curAct->resourceType;
                int numberReq = curAct->numberReq;

                if (curAct->delay-- > 0) {
                    deadlocked = false;
                    //cout<<" Task"<<i+1<<" computes: remaining delay time "<<curAct->delay<<endl;
                }else if (curAct->type == "initiate") {
                    deadlocked = false;
                    tasks[i]->curIndex++;
                    //cout<<" Task"<<i+1<<" completes its initiate"<<endl;
                } else if (curAct->type == "request") {
                    if (resource[resourceType] >= numberReq) {
                        deadlocked = false;
                        tasks[i]->curIndex++;
                        tasks[i]->ownResource[resourceType] += numberReq;
                        resource[resourceType] -= numberReq;
                        //cout<<" Task"<<tasks[i]->taskNum<<" completes its request"<<endl;
                    } else {
                        tasks[i]->status = "blocked";
                        blocked.push_back(tasks[i]);
                        //cout<<" Task"<<tasks[i]->taskNum<<"'s request cannot be granted"<<endl;
                    }
                } else if (curAct->type == "release") {
                    deadlocked = false;
                    released[resourceType] += numberReq;
                    tasks[i]->ownResource[resourceType] -= numberReq;
                    tasks[i]->curIndex++;
                    //cout<<" Task"<<i+1<<" release "<<numberReq<<" "<<"units of "<<resourceType<<" available at "<<cycle + 1<<endl;
                }
                task::activity* nextAct = tasks[i]->activities[tasks[i]->curIndex];
                if (nextAct->type == "terminate" && nextAct->delay == 0) {
                    tasks[i]->timeTaken = cycle + 1;
                    tasks[i]->status="terminated";
                    terminated++;
                    //cout<<" Task"<<i+1<<" is finished at "<<cycle+1<<endl;
                }
            } else if (tasks[i]->status == "abort to active") {
                deadlocked = false;
                tasks[i]->status = "active";
            }
        }
        for (int i = 1; i <= resourceCount; i++) {
            resource[i] += released[i];
        }
        //printResourceStatus();

        abortTask();
        calWaitingTime();
        cycle++;
    }
}

int main(int argc, char* argv[]) {
//    readTasks("example13.txt");
    string fileName(argv[1]);
    readTasks(fileName);
    std::cout << "FIFO" << std::endl;
    FIFO();
    printOutput();
    clearInput();
    //readTasks("example13.txt");
    readTasks(fileName);
    std::cout << "BANKER" << std::endl;
    banker();
    printOutput();
    return 0;
}