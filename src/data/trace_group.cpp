#include <assert.h>

#include "trace_group.h"

Trace_group::Trace_group(std::string name)
 : Tree_item(name)
{
}


Tree_item* Trace_group::get_child(int n)
{
    const int num_subgroups = m_subgroups.size();
    if (n < num_subgroups)
    {
        return m_subgroups[n];
    }
    else
    {
        const int trace_num = n - num_subgroups;
        return m_traces[trace_num];
    }
}


int Trace_group::num_childs() const
{
    return m_subgroups.size() + m_traces.size();
}


void Trace_group::add_trace(Trace_interface* trace)
{
    m_traces.push_back(trace);
    trace->set_parent(this);
}


void Trace_group::add_group(Trace_group* group)
{
    m_subgroups.push_back(group);
    group->set_parent(this);
}
