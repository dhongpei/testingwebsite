create table Login (
	-- General Account Info
	EmailAddress  	 	varchar(30) not null,
	Company				varchar(30) not null foreign key references Disable(Company),
	Username	     	varchar(20) not null,
	Password		 	varchar(25) not null,

	-- 2FA (For later)
	PhoneNumber			varchar(15),
	PhoneExtension		integer,
	NotifyEmail			varchar(1) default 'N' check(NotifyEmail in ('Y', 'N')) not null,
	NotifySMS			varchar(1) default 'N' check(NotifySMS in ('Y', 'N')) not null,
	
	AccountAccess		smallint default 0 not null, 										-- -1(Admin)	0(Base)    1(Manager)   2(Master)

	constraint PK_Login primary key (EmailAddress,Username)
);


create table Disable (
	Company				varchar(30) not null,
	NextPayment			date not null,
	LastPayment			date default getdate(),
	Expired				varchar(1) default 'Y' check(Expired in ('Y', 'N')),

	constraint PK_Disable primary key (Company)
);

create table Passcodes (
	Company				varchar(30) not null foreign key references Disable(Company),
	Code				varchar(8) not null,

	constraint PK_Passcodes primary key (Company, Code)
);


create table Permissions (
	Company				varchar(30) not null foreign key references Disable(Company),
	Username			varchar(20) not null foreign key references Login(Username),
	GroupID				varchar(15) not null,

	constraint PK_Perm primary key (Company,Username,GroupID),
	constraint FK_Perm foreign key (Company,GroupID) references Group (Company,GroupID)
);


create table TGroup (
	Company				varchar(30) not null foreign key references Disable(Company),
	GroupID				varchar(15) not null,

	constraint PK_Group primary key (Company,GroupID)
);


create table Tank (
	Company    			varchar(30) not null foreign key references Disable(Company),	-- Sort by
	GroupID				varchar(30),													-- Sort by, (for later, compound sort with location)
	Location    		varchar(30) not null,											-- 'City, State, Country', Sort by
	TankNo    			varchar(10) not null,											-- Sort by
	TankType			varchar(25) check(TankType in ('Aboveground Vertical', 'Underground Vertical', 'Aboveground Horizontal', 'Underground Horizontal', 'Sphere', 'Rectangular')),
	Shell				varchar(30) check(Shell in ('Bolted', 'Bolted Welded', 'Butt Riveted', 'Butt Riveted Insulated', 'Butt Riveted Seal Welded', 'Butt Welded', 'Butt Welded Insulated', 'Insulated', 'Lap Riveted', 'Lap Riveted Insulated', 'Lap Riveted Seal Welded', 'Lap Welded', 'Lap Welded Insulated', 'Riveted/Combination Welded', 'Unknown')),
	Roof				varchar(25) check(Roof in ('Aluminum Dome', 'Cone', 'Cone Insulated', 'Dome', 'Open Top', 'Self-Supported Insulated', 'Self-Supporting Cone', 'Unknown')),
	Floating			varchar(40) check(Floating in ('Aluminum', 'Aluminum Foam Float', 'Aluminum Honey Comb', 'Aluminum Pipe Pontoon', 'Annular Pontoon', 'Annular Pontoon Intermediate Deck', 'Annular Pontoon Insulated', 'Annular Pontoon Reverse Slope', 'Annular Pontoon with Center Pontoon', 'Double Deck', 'Double Deck Insulated', 'External FR', 'None', 'Steel Pan', 'Steel Pan with Open Pontoons', 'Unknown')),
	Bottom				varchar(30) check(Bottom in ('Bolted', 'Butt Welded', 'Double', 'Double with Annular Plate', 'Lap Welded Single', 'Riveted', 'Single with Annular Plate', 'Triple', 'Triple with Annular Plate', 'Unknown')),
	Foundation			varchar(20) check(Foundation in ('Asphalt', 'Concrete Ring Wall', 'Concrete Saddle', 'Concrete Slab', 'Crushed Stone', 'Earthen', 'Sand', 'Steel Bearing Plate', 'Steel Saddle', 'Unknown')),
	Product    			varchar(25) check(Product in ('Additive for Gasoline', 'Anhydrous Ammonia', 'Asphalt', 'Av Gas', 'Bio Diesel', 'Black Oil', 'Caustic', 'Crude', 'Diesel', 'Diesel (Fuel Oil 1-D)', 'Diesel (Fuel Oil 2-D)', 'Diesel Low Sulfur', 'Diesel Marine F-76', 'E-85', 'Ethanol', 'F-76', 'Fertilizer', 'Fertilizer UAN 32', 'Fuel Oil', 'Fuel Oil No. 1', 'Fuel Oil No. 2', 'Fuel Oil No. 4', 'Fuel Oil No. 5', 'Fuel Oil No. 6', 'Gas Oil', 'Gasoline', 'Jet', 'Jet A', 'JP-4', 'JP-5', 'JP-8', 'Kerosene', 'Lexorez 1102', 'Lignin', 'Methanol', 'Naphtha (Petroleum)', 'Naphtha (Solvent)', 'Naphtha VM & P', 'Out of Service', 'Regular Gasoline', 'Rerun Alkylate', 'Sulfuric Acid', 'Ultra Low Diesel', 'Unknown', 'Waste Coolant', 'Waste Water', 'Water', 'Wax')),
																						-- Sort by
	Diameter			decimal check (Diameter > 0),									-- ft
	Height				decimal check (Height > 0),										-- ft
	Capacity    		decimal check (Capacity > 0),									-- BBL's, Sort by?

	-- To Be Added
	LastExternal    		date,														-- Sort by
	ExpExternal    			date, 														-- Sort by
	LastInternal    		date, 														-- Sort by
	ExpInternal    			date, 														-- Sort by
	LastUT    				date, 														-- Sort by
	ExpUT    				date, 														-- Sort by
	ConditionComments   	varchar(300),												-- Current issues, potential problems/predictions (age, location/geography, etc.)
	Recommendations     	varchar(300),												-- Needed changes, determines need of periodic checks/reports

	-- Unimplemented Info
	Address    				varchar(100),												-- Not including macro location, Sort by
	Latitude				decimal,
	Longitude				decimal,
	OperatingHeight			decimal,													-- ft
	Constructed    			smallint check(Constructed > 1500 and Constructed < 3000),  -- Sort by
	APIStandard				varchar(10),
	Manufacturer    		varchar(30),												-- Sort by?
	WindSpeed				decimal,													-- unit?
	Altitude				decimal,													-- unit?
	Seismic					decimal,													-- unit?
	Material				varchar(30),
	WeldJointEff			decimal,
	StorageTemp				decimal,													-- F
	VaporPressure			decimal,
	SpecificGravity			decimal,
	BoilingPoint			decimal,													-- F
	FlashPoint				decimal,													-- F
	LatentHeatVapor			decimal,													-- BTU/Lb
	CriticalTemp			decimal,													-- F
	NFPAClass    			varchar(2) check(NFPAClass in ('1A', '1B', '1C', '2', '3A', '3B')),
																						-- Sort by?
	SuctionSize				decimal,													-- in
	SuctionCount			integer,
	RecieptSize				decimal,													-- in
	RecieptCount			integer,
	LowSuctionSize			decimal,													-- in
	LowSuctionCount			integer,
	WaterDrawSize			decimal,													-- in
	WaterDrawCount			integer,
	ShellManwaySize			decimal,													-- in
	ShellManwayCount		integer,
	ShellMixerSize			decimal,													-- in
	ShellMixerCount			integer,
	SwingLineType    		varchar(10) check(SwingLineType in ('None', 'Unknown', 'Swing Line', 'Float', 'Winch')),
	ShellOverflow			varchar(1) check(ShellOverflow in ('Y', 'N')),
	DoubleBottHeight		decimal,													-- unit?
	CourseCount				integer,
	CourseHeight    		decimal,													-- ft
	VertWeldSpacing    		decimal,													-- in,
	ExtCoating				varchar(15),												-- options?
	ExtCoatingDate    		date,														-- Sort by
	IntCoating				varchar(15),												-- options?
	IntCoatingDate    		date,														-- Sort by
	BottCoating				varchar(15),												-- options?
	BottCoatingDate			date,														-- Sort by
	FixedRoofCoating		varchar(15),												-- options?
	FixedRoofCoatingDate	date,														-- Sort by
	FloatRoofCoating		varchar(15),												-- options?
	FloatRoofCoatingDate	date,														-- Sort by
	Insulation    			varchar(10) check(Insulation in ('None', 'Unknown', 'Insulated', 'Sprayed')),
	InsulationDate    		date,														-- Sort by
	
	constraint PK_Tank primary key (Company,Location,TankNo)
);


"""
WIP
"""
create table Files (
	Company					varchar(30) not null foreign key references Disable(Company),
	Location				varchar(30) not null,
	TankNo					varchar(10) not null,
	FileName				varchar(100) not null,
	
	
	constraint PK_Files primary key (FileName),
	constraint FK_Files foreign key (Company,Location,TankNo) references Tank (Company,Location,TankNo)
);