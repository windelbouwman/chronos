#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    m_aboutAct = new QAction("About");

    createMenus();
    createDockWindows();

    m_signal_viewer = new SignalViewer(this);
    setCentralWidget(m_signal_viewer);
}

MainWindow::~MainWindow()
{
    delete m_data_sources_view;
    delete m_timespan_selector;

    delete m_aboutAct;

    delete ui;
}

void MainWindow::createMenus()
{
    m_viewMenu = menuBar()->addMenu("View");

    QMenu* fileMenu = menuBar()->addMenu(tr("Help"));
    fileMenu->addAction(m_aboutAct);
}

void MainWindow::createDockWindows()
{
    // Create the data sources widget:
    QDockWidget *data_source_dock = new QDockWidget("Available signals", this);
    data_source_dock->setAllowedAreas(Qt::AllDockWidgetAreas | Qt::RightDockWidgetArea);
    m_data_sources_view = new SourcesSelector(data_source_dock);
    data_source_dock->setWidget(m_data_sources_view);
    addDockWidget(Qt::LeftDockWidgetArea, data_source_dock);
    m_viewMenu->addAction(data_source_dock->toggleViewAction());

    // Create the timespan widget:
    QDockWidget *timespan_dock = new QDockWidget("Selected timespan", this);
    timespan_dock->setAllowedAreas(Qt::AllDockWidgetAreas);
    m_timespan_selector = new TimespanSelectionWidget(timespan_dock);
    timespan_dock->setWidget(m_timespan_selector);
    addDockWidget(Qt::TopDockWidgetArea, timespan_dock);
    m_viewMenu->addAction(timespan_dock->toggleViewAction());
}
