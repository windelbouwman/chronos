#ifndef DATA_SOURCE_H
#define DATA_SOURCE_H

#include <vector>
#include "src/data/trace_group.h"

class Data_source
{
public:
    Data_source(std::string name);
    Trace_group* get_root() const;

private:
    Trace_group* m_root_group;
};

#endif // DATA_SOURCE_H
