#include "tree_item.h"

#include <string>
#include <assert.h>


Tree_item::Tree_item(std::string name)
    : m_name(name),
      m_parent(0)
{

}


std::string Tree_item::get_name()
{
    return m_name;
}


Tree_item* Tree_item::get_parent()
{
    return m_parent;
}


void Tree_item::set_parent(Tree_item* parent)
{
    m_parent = parent;
}


bool Tree_item::is_root()
{
    return m_parent == 0;
}


int Tree_item::row()
{
    // Naive implementation that looksup the row
    assert(m_parent);

    for (int i = 0; i < m_parent->num_childs(); i++)
    {
        if (m_parent->get_child(i) == this)
        {
            return i;
        }
    }

    // We should never reach this point!
    assert(0);
}
