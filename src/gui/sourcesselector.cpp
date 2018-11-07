#include "sourcesselector.h"

#include <QObject>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QTreeView>
#include <QSortFilterProxyModel>


SourcesSelector::SourcesSelector(QWidget *parent) : QWidget(parent)
{
    m_data_sources_model = new DataSourceModel();

    setupGui();


    // m_data_sources_view->expandAll();
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

    QPushButton* expandAll = new QPushButton("Expand all", this);
    layout->addWidget(expandAll);

    m_data_sources_view = new QTreeView(this);
    layout->addWidget(m_data_sources_view);

    connect(expandAll, &QPushButton::clicked, m_data_sources_view, &QTreeView::expandAll);

    setLayout(layout);

    // Hookup some extra signals and slots:
    QSortFilterProxyModel* filter_model = new QSortFilterProxyModel;
    filter_model->setSourceModel(m_data_sources_model);
    filter_model->setFilterCaseSensitivity(Qt::CaseInsensitive);
    m_data_sources_view->setModel(filter_model);

    connect(signal_filter, &QLineEdit::textChanged, filter_model, &QSortFilterProxyModel::setFilterFixedString);
}
