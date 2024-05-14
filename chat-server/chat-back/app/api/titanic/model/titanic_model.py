from dataclasses import dataclass
import numpy as np
import pandas as pd
from app.api.context.data_sets import DataSets
from app.api.context.models import Models

class TitanicModel(object):

    model = Models()
    dataset = DataSets()

    def preprocess(self, train_fname, test_fname) -> object:
        this = self.model
        that = self.dataset

        this.ds.train = self.new_model(train_fname)
        this.ds.test = self.new_model(test_fname)
        feature = ['PassengerId','Survived','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']
        # 데이터셋은 Train과 Test, Validation 3종류로 나뉘어져 있다.
        this.train = that.new_dframe(train_fname)
        this.test = that.new_dframe(test_fname)
        this.id = this.test['PassengerId']
        this.lable = this.train['Survived']
        this.train = this.train.drop(['Survived'], axis=1)
        this = self.drop_feature(this, 'SibSp', 'Parch', 'Ticket', 'Cabin')
        
        return this.dataset
    
    @staticmethod
    def drop_feature(this, *feature) -> object:
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train_model, this.test_model]]
        return this
    
    @staticmethod
    def remove_duplicate_title(this) -> pd.DataFrame:
        a = []
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        print(a)
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr' : 1, 'Ms': 2, 'Mrs' : 3 ,'Master' : 4, 'Royal' : 5, 'Rare' : 6}
        return title_mapping
    
    @staticmethod
    def title_nominal(this, title_mapping) -> pd.DataFrame:
        for these in [this.train, this.test]:
            these['Title'] = these['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)
        return this
    
    @staticmethod
    def age_ratio(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        age_mapping = {'Unknown':0 , 'Baby': 1, 'Child': 2, 'Teenager' : 3, 'Student': 4,
                       'Young Adult': 5, 'Adult':6,  'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5) # 왜 NaN 값에 -0.5 를 할당할까요 ?
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf] # 이것을 이해해보세요
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']

        for these in train, test:
            pass # pd.cut() 을 사용하시오. 다른 곳은 고치지 말고 다음 두 줄만 완성하시오
            these['Age'] = pd.cut(these['Age'], bins, labels=labels)
            these['AgeGroup'] = these['Age'].map(age_mapping)#map() 사용

        return this