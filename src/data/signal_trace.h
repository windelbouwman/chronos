#ifndef SIGNAL_TRACE_H
#define SIGNAL_TRACE_H

#include <string>
#include <vector>
#include <tuple>
#include "trace_interface.h"


class Signal_trace : public Trace_interface
{
public:
    Signal_trace(std::string name);

    virtual Tree_item* get_child(int n);
    virtual int num_childs() const;

    void add_point(double x, double y);

private:
    std::vector<std::tuple<double, double>> m_points;
};

#endif // SIGNAL_TRACE_H
