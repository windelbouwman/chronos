#include "sourcesselector.h"

#include <QVBoxLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QTreeView>
#include <QSortFilterProxyModel>


SourcesSelector::SourcesSelector(QWidget *parent) : QWidget(parent)
{
    m_data_sources_model = new DataSourceModel();

    setupGui();

    QSortFilterProxyModel* filter_model = new QSortFilterProxyModel;
    // filter_model->
    m_data_sources_view->setModel(m_data_sources_model);
}

SourcesSelector::~SourcesSelector()
{
    delete m_data_sources_model;
}

void SourcesSelector::setupGui()
{
    QVBoxLayout* layout = new QVBoxLayout(this);

    QLineEdit* signal_filter = new QLineEdit(this);
    layout->addWidget(signal_filter);

    m_data_sources_view = new QTreeView(this);
    layout->addWidget(m_data_sources_view);

    setLayout(layout);
}
