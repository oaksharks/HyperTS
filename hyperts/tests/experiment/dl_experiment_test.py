import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from hyperts.datasets import load_network_traffic, load_arrow_head, load_basic_motions
from hyperts.utils import consts, metrics
from hyperts.utils._base import get_tool_box
from hyperts.experiment import make_experiment, process_test_data

class Test_Experiment():

    def test_univariate_forecast(self):
        df = load_network_traffic(univariate=True)
        tb = get_tool_box(df)
        train_df, test_df = tb.temporal_train_test_split(df, test_size=0.1)

        timestamp = 'TimeStamp'
        covariables = ['HourSin', 'WeekCos', 'CBWD']
        task = consts.Task_FORECAST
        reward_metric = metrics.smape
        optimize_direction = consts.OptimizeDirection_MINIMIZE

        exp = make_experiment(train_df.copy(),
                              mode='dl',
                              timestamp=timestamp,
                              covariables=covariables,
                              task=task,
                              callbacks=None,
                              reward_metric=reward_metric,
                              optimize_direction=optimize_direction)

        model = exp.run(max_trials=3)

        X_test, y_test = process_test_data(test_df, timestamp=timestamp, covariables=covariables, impute=True)

        y_pred = model.predict(X_test)
        assert y_pred.shape == y_test.shape
        score = metrics.mape(y_test, y_pred)
        print('univariate_forecast mape: ', score)

    def test_multivariate_forecast(self):
        df = load_network_traffic()
        tb = get_tool_box(df)
        train_df, test_df = tb.temporal_train_test_split(df, test_size=0.1)

        timestamp = 'TimeStamp'
        covariables = ['HourSin', 'WeekCos', 'CBWD']
        task = consts.Task_MULTIVARIATE_FORECAST
        reward_metric = consts.Metric_RMSE
        optimize_direction = consts.OptimizeDirection_MINIMIZE

        exp = make_experiment(train_df.copy(),
                              mode='dl',
                              timestamp=timestamp,
                              covariables=covariables,
                              task=task,
                              callbacks=None,
                              reward_metric=reward_metric,
                              optimize_direction=optimize_direction)

        model = exp.run(max_trials=3)

        X_test, y_test = process_test_data(test_df, timestamp=timestamp, covariables=covariables, impute=True)

        y_pred = model.predict(X_test)
        assert y_pred.shape == y_test.shape
        score = metrics.mape(y_test, y_pred)
        print('multivariate_forecast mape: ', score)

    def test_univariate_classification(self):
        df = load_arrow_head()
        tb = get_tool_box(df)
        train_df, test_df = tb.random_train_test_split(df, test_size=0.2)

        target = 'target'
        task = consts.Task_CLASSIFICATION
        reward_metric = consts.Metric_ACCURACY
        optimize_direction = consts.OptimizeDirection_MAXIMIZE

        exp = make_experiment(train_df.copy(),
                              mode='dl',
                              task=task,
                              eval_data=test_df.copy(),
                              target=target,
                              reward_metric=reward_metric,
                              optimize_direction=optimize_direction)

        model = exp.run(max_trials=3)

        X_test, y_test = process_test_data(test_df, target=target)

        y_pred = model.predict(X_test)

        score = metrics.accuracy_score(y_test, y_pred)

        assert score > 0
        print('univariate_classification accuracy:  {} %'.format(score*100))

    def test_multivariate_classification(self):
        df = load_basic_motions()
        tb = get_tool_box(df)
        train_df, test_df = tb.random_train_test_split(df, test_size=0.2)

        target = 'target'
        task = consts.Task_CLASSIFICATION
        reward_metric = metrics.f1_score
        optimize_direction = consts.OptimizeDirection_MAXIMIZE

        exp = make_experiment(train_df.copy(),
                              mode='dl',
                              task=task,
                              eval_data=test_df.copy(),
                              target=target,
                              reward_metric=reward_metric,
                              optimize_direction=optimize_direction)

        model = exp.run(max_trials=3)

        X_test, y_test = process_test_data(test_df, target=target)

        y_pred = model.predict(X_test)

        score = metrics.accuracy_score(y_test, y_pred)

        assert score > 0
        print('multivariate_classification accuracy:  {} %'.format(score*100))