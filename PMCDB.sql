##############################################################################
# 							PMC Database script 							 #
##############################################################################

#Dropping Database if exists and Creating new Database 
DROP database IF EXISTS pmc_db;
CREATE database pmc_db;
USE pmc_db;
SET AUTOCOMMIT=0;

#Dropping Table if exists and Creating new Manufacturer Table 
DROP TABLE IF EXISTS Manufacturer;
CREATE TABLE Manufacturer (
  ManufacturerName varchar(50),
  ManufactuerAuthority varchar(50) not null,
  PhoneNumber varchar(12) not null unique,
  Address varchar(250) not null,
  EmaiID varchar(50) not null unique,
  username varchar(50) not null unique,
  password varchar(50) not null,
    PRIMARY KEY (ManufacturerName)
  );
  
#Dropping Table if exists and Creating new Product Table 
DROP TABLE IF EXISTS Product;
CREATE TABLE Product (
  ProductModel varchar(50),
  ManufacturerName varchar(50),
  ModuleTechnology varchar(50) not null,
  ManufacturedDate date not null,
  mIsc float not null,
  mVoc float not null,
  mImp float not null,
  mVmp float not null,
  mFF  float not null,
  mPmp float not null,
    PRIMARY KEY (ProductModel),
    FOREIGN KEY (ManufacturerName) references Manufacturer(ManufacturerName)
 );
 

#Dropping Table if exists and Creating new Testlab Table  
DROP TABLE IF EXISTS TestLab;
CREATE TABLE TestLab (
  TestLabName varchar(50),
  TestLabAuthority varchar(50) not null,
  PhoneNumber varchar(12) not null unique,
  Address varchar(300) not null,
  EmaiID varchar(50) not null unique,
  username varchar(50) not null unique,
  password varchar(50) not null,
    PRIMARY KEY (TestLabName)
  );
 
 #Dropping Table if exists and Creating new CertificationAccess Table 
 DROP TABLE IF EXISTS CertificationAccess;
 CREATE TABLE CertificationAccess (
  ManufacturerName varchar(50),
  ProductModel varchar(50),
  AllowUserAccess boolean,
    FOREIGN KEY (ManufacturerName) references Manufacturer(ManufacturerName),
    FOREIGN KEY (ProductModel) references Product(ProductModel)
);

#Dropping Table if exists and Creating new Tests Table 
DROP TABLE IF EXISTS Tests;
CREATE TABLE Tests (
  ProjectNo  int(16) auto_increment,
  ProductModel varchar(50),
  TestLabName varchar(50),
    PRIMARY KEY (ProjectNo)
);
ALTER TABLE Tests AUTO_INCREMENT=1001;

#Dropping Table if exists and Creating new Samples Table 
DROP TABLE IF EXISTS Samples;
CREATE TABLE Samples (
  ProjectNo  int(16),
  SampleID varchar(50),
	FOREIGN KEY (ProjectNo) references Tests(ProjectNo),
    PRIMARY KEY (ProjectNo,SampleID)
);

#Dropping Table if exists and Creating new TestResults Table 
DROP TABLE IF EXISTS TestResults;  
CREATE TABLE TestResults (
  ProjectNo  int(16),
  SampleID varchar(50),
  Sequence char not null,
  TestName varchar(50) not null,
  TestDate date not null,
  tIsc float not null,
  tVoc float not null,
  tImp float not null,
  tVmp float not null,
  tFF  float not null,
  tPmp float not null,
    FOREIGN KEY (ProjectNo, SampleID) references Samples(ProjectNo,SampleID),
    PRIMARY KEY (ProjectNo,Sequence, SampleID)    
 );
 
#Dropping Table if exists and Creating new TestReport Table 
DROP TABLE IF EXISTS TestReport;
CREATE TABLE TestReport (
  ProjectNo  int(16),
  Sequence char,
  Verdict varchar(50) not null,
   FOREIGN KEY (ProjectNo,Sequence) references TestResults(ProjectNo,Sequence)
  -- FOREIGN KEY (Sequence) references TestResults(Sequence)
);

#Dropping Table if exists and Creating new SummaryReport Table 
DROP VIEW IF EXISTS SummaryReport;
CREATE VIEW SummaryReport AS
SELECT Tests.ProductModel,TestReport.Sequence,TestReport.Verdict FROM TestReport LEFT JOIN Tests
	ON (TestReport.ProjectNo = Tests.ProjectNo);
    
#Dropping Table if exists and Creating new Certification Table 
DROP VIEW IF EXISTS Certification;
CREATE VIEW Certification AS
SELECT distinct Tests.ProductModel,TestReport.Verdict FROM TestReport LEFT JOIN Tests
	ON (TestReport.ProjectNo = Tests.ProjectNo) where verdict ='FAIL'
union
SELECT distinct Tests.ProductModel,TestReport.Verdict FROM TestReport LEFT JOIN Tests
	ON (TestReport.ProjectNo = Tests.ProjectNo) where Tests.ProductModel not in (SELECT distinct Tests.ProductModel FROM TestReport LEFT JOIN Tests
	ON (TestReport.ProjectNo = Tests.ProjectNo) where verdict ='FAIL') 
order by ProductModel;

show tables;
    