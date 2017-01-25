#ifndef SOURCESSELECTOR_H
#define SOURCESSELECTOR_H

#include <QWidget>
#include <QTreeView>

#include "datasourcemodel.h"


class SourcesSelector : public QWidget
{
    Q_OBJECT
public:
    explicit SourcesSelector(QWidget *parent = 0);
    ~SourcesSelector();

signals:

public slots:
private:
    void setupGui();

    QTreeView* m_data_sources_view;
    DataSourceModel* m_data_sources_model;
};

#endif // SOURCESSELECTOR_H
