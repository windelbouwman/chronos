#include "timespanselectionwidget.h"

#include <QPushButton>
#include <QVBoxLayout>

TimespanSelectionWidget::TimespanSelectionWidget(QWidget *parent) : QWidget(parent)
{
    QPushButton* last_minute = new QPushButton("Last minute", this);
    QPushButton* last_week = new QPushButton("Last week", this);
    QVBoxLayout* layout = new QVBoxLayout(this);
    layout->addWidget(last_minute);
    layout->addWidget(last_week);
    setLayout(layout);
}
