#include "datasourcemodel.h"

// Check this out: http://doc.qt.io/qt-5/qtwidgets-itemviews-simpletreemodel-example.html

DataSourceModel::DataSourceModel()
    : QAbstractItemModel()
{

}

QModelIndex DataSourceModel::index(int row, int column, const QModelIndex& parent) const
{

}

QModelIndex DataSourceModel::parent(const QModelIndex& parent) const
{
    if (!parent.isValid())
    {
        return QModelIndex();
    }

    return QModelIndex();

    // return createIndex(0, 0);
}

int DataSourceModel::rowCount(const QModelIndex& parent) const
{
    return 0;
}

int DataSourceModel::columnCount(const QModelIndex& parent) const
{
    return 2;
}

QVariant DataSourceModel::data(const QModelIndex &index, int role) const
{
}
