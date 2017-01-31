#include "data_source.h"

Data_source::Data_source(std::string name)
{
    m_root_group = new Trace_group(name);
}

Trace_group* Data_source::get_root() const
{
    return m_root_group;
}
