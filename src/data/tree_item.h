#ifndef TREE_ITEM_H
#define TREE_ITEM_H

#include <string>

class Tree_item
{
public:
    Tree_item(std::string name);

    virtual Tree_item* get_child(int n) = 0;
    virtual int num_childs() const = 0;

    std::string get_name();

    Tree_item* get_parent();
    void set_parent(Tree_item*);
    bool is_root();

    int row();

private:
    std::string m_name;
    Tree_item* m_parent;
};

#endif // TREE_ITEM_H
