#ifndef DATASOURCEMODEL_H
#define DATASOURCEMODEL_H

#include <QAbstractItemModel>
#include "src/data/data_source.h"


class DataSourceModel : public QAbstractItemModel
{
public:
    DataSourceModel();

    virtual QModelIndex index(int row, int column, const QModelIndex& parent) const;
    virtual QModelIndex parent(const QModelIndex& parent) const;
    virtual int rowCount(const QModelIndex& parent) const;
    virtual int columnCount(const QModelIndex& parent) const;
    virtual QVariant data(const QModelIndex &index, int role) const;

private:
    void create_test_set();
    Data_source m_datasource;
};


#endif // DATASOURCEMODEL_H
