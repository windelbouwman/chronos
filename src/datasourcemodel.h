#ifndef DATASOURCEMODEL_H
#define DATASOURCEMODEL_H

#include <QAbstractItemModel>


class DataSourceModel : public QAbstractItemModel
{
public:
    DataSourceModel();

    virtual QModelIndex index(int row, int column, const QModelIndex& parent) const;
    virtual QModelIndex parent(const QModelIndex& parent) const;
    virtual int rowCount(const QModelIndex& parent) const;
    virtual int columnCount(const QModelIndex& parent) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
};


class DataSet
{
public:
    QString name;
};


#endif // DATASOURCEMODEL_H
