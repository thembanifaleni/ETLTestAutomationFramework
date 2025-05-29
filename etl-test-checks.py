import pytest
import pandas as pd

# ------------------------------
# Fixtures to isolate data loading
# ------------------------------
@pytest.fixture
def target_df():
    return pd.read_csv("target.csv", sep=",")

@pytest.fixture
def source_df():
    return pd.read_csv("source.csv")

# ------------------------------
# Test for duplicate records
# ------------------------------
def test_checkDuplicates(target_df):
    count = target_df.duplicated().sum()
    assert count == 0, "Duplication found - please verify the target"

# ------------------------------
# Test for data completeness
# ------------------------------
def test_DataCompleteness(target_df):
    assert not target_df.empty, "Target file is empty - please verify the ETL process"

# ------------------------------
# Test for mandatory 'deptno' column (null check)
# ------------------------------
def test_deptNoForNullValueCheck(target_df):
    isDeptNoNULL = target_df['deptno'].isnull().any()
    assert not isDeptNoNULL, "deptno is having a null value - Please check"

# ------------------------------
# Test if 'eno' is a unique identifier (primary key)
# ------------------------------
def test_enoNoForUniqueValueCheck(target_df):
    totalCount = target_df['eno'].count()
    uniqueCount = target_df['eno'].nunique()
    assert totalCount == uniqueCount, "eno column values are not unique .. please check"

# ------------------------------
# Test for column name transformation
# ------------------------------
def test_columnNameTransformation(source_df, target_df):
    assert 'employee_no' in source_df.columns
    assert 'eno' in target_df.columns

    assert 'employee_name' in source_df.columns
    assert 'ename' in target_df.columns

    assert 'department_number' in source_df.columns
    assert 'deptno' in target_df.columns

    assert 'salary' in source_df.columns
    assert 'Salary' in target_df.columns

# ------------------------------
# Test if row count matches between source and target
# ------------------------------
def test_rowCountMatch(source_df, target_df):
    assert len(source_df) == len(target_df), "Record count mismatch between source and target"

# ------------------------------
# Test if 'eno' values match from source to target
# ------------------------------
def test_enoMapping(source_df, target_df):
    assert all(source_df['employee_no'].values == target_df['eno'].values), "Mismatch in eno mapping from source"

# ------------------------------
# Test if 'deptno' values match from source to target
# ------------------------------
def test_deptnoMapping(source_df, target_df):
    assert all(source_df['department_number'].values == target_df['deptno'].values), "Mismatch in deptno mapping from source"

# ------------------------------
# Test if 'Salary' values match from source to target
# ------------------------------
def test_salaryTransformation(source_df, target_df):
    assert all(source_df['salary'].values == target_df['Salary'].values), "Mismatch in Salary values between source and target"
