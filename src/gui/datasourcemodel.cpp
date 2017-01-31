#include "datasourcemodel.h"

#include <math.h>

#include "src/data/trace_interface.h"
#include "src/data/trace_group.h"
#include "src/data/signal_trace.h"

// Check this out: http://doc.qt.io/qt-5/qtwidgets-itemviews-simpletreemodel-example.html

DataSourceModel::DataSourceModel()
    : QAbstractItemModel(),
      m_datasource("demodata")
{
   create_test_set();
}


void DataSourceModel::create_test_set()
{
    // Prepare some dummy data:
    Trace_group* root = m_datasource.get_root();

    Trace_group* group1 = new Trace_group("group1");
    root->add_group(group1);

    Trace_group* subgroup1 = new Trace_group("part1");
    group1->add_group(subgroup1);

    Signal_trace* trace101 = new Signal_trace("Sig101");
    subgroup1->add_trace(trace101);

    Signal_trace* trace1 = new Signal_trace("Sig1");
    group1->add_trace(trace1);
    for (int i=0; i<100; i++)
    {
        trace1->add_point(i, sin(i));
    }

    Trace_interface* trace2 = new Signal_trace("Sig2");
    group1->add_trace(trace2);

    Trace_group* group2 = new Trace_group("Group2");
    root->add_group(group2);
}


QModelIndex DataSourceModel::index(int row, int column, const QModelIndex& parent) const
{
    if (!hasIndex(row, column, parent))
    {
        return QModelIndex();
    }

    Tree_item* parent_item;
    if (parent.isValid())
    {
        parent_item = static_cast<Tree_item*>(parent.internalPointer());
    }
    else
    {
        // Parent is root item!
        parent_item = m_datasource.get_root();
    }

    Tree_item* item = parent_item->get_child(row);
    return createIndex(row, column, item);
}

QModelIndex DataSourceModel::parent(const QModelIndex& index) const
{
    if (!index.isValid())
    {
        return QModelIndex();
    }

    Tree_item* item = static_cast<Tree_item*>(index.internalPointer());
    Tree_item* parent_item = item->get_parent();

    if (parent_item->is_root())
    {
        return QModelIndex();
    }
    else
    {
        return createIndex(parent_item->row(), 0, parent_item);
    }
}

int DataSourceModel::rowCount(const QModelIndex& parent) const
{
    Tree_item* parent_item;

    if (parent.isValid())
    {
        parent_item = static_cast<Tree_item*>(parent.internalPointer());

    }
    else
    {
        // Tha root item!
        parent_item = m_datasource.get_root();
    }

    return parent_item->num_childs();
}

int DataSourceModel::columnCount(const QModelIndex& parent) const
{
    return 2;
}

QVariant DataSourceModel::data(const QModelIndex &index, int role) const
{
    if (index.isValid())
    {
        if (role == Qt::DisplayRole)
        {
            Tree_item* item = static_cast<Tree_item*>(index.internalPointer());

            if (index.column() == 0)
            {
                return QVariant(item->get_name().c_str());
            }
        }
        else
        {
            return QVariant();
        }
    }
    else
    {
        return QVariant();
    }
}
