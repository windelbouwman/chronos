#include <assert.h>
#include "signal_trace.h"


Signal_trace::Signal_trace(std::string name)
    : Trace_interface(name)
{
}


Tree_item* Signal_trace::get_child(int n)
{
    assert(0);
}


int Signal_trace::num_childs() const
{
    return 0;
}


void Signal_trace::add_point(double x, double y)
{
    m_points.push_back(std::tuple<double, double>(x,y));
}
