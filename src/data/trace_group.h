#ifndef TRACE_GROUP_H
#define TRACE_GROUP_H

#include <vector>
#include <string>
#include "src/data/trace_interface.h"
#include "src/data/trace_group.h"
#include "src/data/tree_item.h"


class Trace_group : public Tree_item
{
public:
    Trace_group(std::string name);

    virtual Tree_item* get_child(int n);
    virtual int num_childs() const;

    void add_trace(Trace_interface*);
    void add_group(Trace_group*);

private:
    std::vector<Trace_group*> m_subgroups;
    std::vector<Trace_interface*> m_traces;
};

#endif // TRACE_GROUP_H
