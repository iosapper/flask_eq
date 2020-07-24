from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from app import login_manager


class Eqinfo(db.Model):
    __tablename__ = 'eqinfo'

    __table_args__ = (
        db.ForeignKeyConstraint(['eqid', 'eqname'], ['eqname.eqid', 'eqname.eqname'], ondelete='CASCADE', onupdate='CASCADE'),
        db.ForeignKeyConstraint(['ksid'], ['keshi.id'], ondelete='CASCADE', onupdate='CASCADE'),
        db.Index('e', 'eqid', 'eqname')
    )

    id = db.Column(db.Integer, primary_key=True)
    ksid = db.Column(db.Integer)
    eqid = db.Column(db.String(10), nullable=True)
    eqname = db.Column(db.String(10), nullable=True)
    eqprdata = db.Column(db.Date, nullable=True)
    equsedata = db.Column(db.Date, nullable=True)
    eqce1filename = db.Column(db.String(255), nullable=True)
    eqce1file_url = db.Column(db.String(255), nullable=True)
    eqce2filename = db.Column(db.String(255), nullable=True)
    eqce2file_url = db.Column(db.String(255), nullable=True)
    eqce3filename = db.Column(db.String(255), nullable=True)
    eqce3file_url = db.Column(db.String(255), nullable=True)
    eqce4filename = db.Column(db.String(255), nullable=True)
    eqce4file_url = db.Column(db.String(255), nullable=True)
    eqce5filename = db.Column(db.String(255), nullable=True)
    eqce5file_url = db.Column(db.String(255), nullable=True)

    eqname1 = db.relationship('Eqname', primaryjoin='and_(Eqinfo.eqid == Eqname.eqid, Eqinfo.eqname == Eqname.eqname)', backref='eqinfos')

    def __init__(self, ksid, eqid,eqname,eqprdata,equsedata,eqce1filename,eqce1file_url,eqce2filename,eqce2file_url,eqce3filename,eqce3file_url,eqce4filename,eqce4file_url,eqce5filename,eqce5file_url):
        self.ksid = ksid
        self.eqid = eqid
        self.eqname =eqname
        self.eqprdata = eqprdata
        self.equsedata = equsedata
        self.eqce1filename =eqce1filename
        self.eqce1file_url =eqce1file_url
        self.eqce2filename =eqce2filename
        self.eqce2file_url =eqce2file_url
        self.eqce3filename =eqce3filename
        self.eqce3file_url =eqce3file_url
        self.eqce4filename =eqce4filename
        self.eqce4file_url =eqce4file_url
        self.eqce5filename =eqce5filename
        self.eqce5file_url =eqce5file_url

    def save(self):
        db.session.add(self)
        db.session.commit()

class Eqname(db.Model):
    __tablename__ = 'eqname'
    __table_args__ = (
        db.ForeignKeyConstraint(['ksid'], ['keshi.id'], ondelete='CASCADE', onupdate='CASCADE'),
        db.Index('eqid', 'eqid', 'eqname'),
    )

    id = db.Column(db.Integer, primary_key=True)
    ksid = db.Column(db.Integer)
    eqid = db.Column(db.String(10), nullable=True)
    eqname = db.Column(db.String(10), nullable=True)
    eqmt = db.Column(db.String(255), nullable=True)

    def __init__(self, ksid,eqid,eqname):
        self.ksid = ksid
        self.eqid = eqid
        self.eqname =eqname


    def save(self):
        db.session.add(self)
        db.session.commit()

class Ininfo(db.Model):
    __tablename__ = 'ininfo'
    __table_args__ = (
        db.ForeignKeyConstraint(['eqid', 'eqname'], ['eqname.eqid', 'eqname.eqname'], ondelete='CASCADE', onupdate='CASCADE'),
        db.ForeignKeyConstraint(['ksid'], ['keshi.id'], ondelete='CASCADE', onupdate='CASCADE'),
        db.Index('e', 'eqid', 'eqname')
    )

    id = db.Column(db.Integer, primary_key=True)
    ksid = db.Column(db.Integer)
    eqid = db.Column(db.String(10), nullable=True)
    eqname = db.Column(db.String(10), nullable=True)
    prid = db.Column(db.String(255), nullable=True)
    smjfilename = db.Column(db.String(255), nullable=True)
    smjfile_url = db.Column(db.String(255), nullable=True)

    eqname1 = db.relationship('Eqname', primaryjoin='and_(Ininfo.eqid == Eqname.eqid, Ininfo.eqname == Eqname.eqname)', backref='ininfos')

    def __init__(self,ksid, eqid,eqname,prid,smjfilename,smjfile_url):
        self.ksid = ksid
        self.eqid = eqid
        self.eqname = eqname
        self.prid = prid
        self.smjfilename = smjfilename
        self.smjfile_url = smjfile_url

    def save(self):
        db.session.add(self)
        db.session.commit()


class Maininfo(db.Model):
    __tablename__ = 'maininfo'
    __table_args__ = (
        db.ForeignKeyConstraint(['eqid', 'eqname'], ['eqname.eqid', 'eqname.eqname'], ondelete='CASCADE', onupdate='CASCADE'),
        db.ForeignKeyConstraint(['ksid'], ['keshi.id'], ondelete='CASCADE', onupdate='CASCADE'),
        db.Index('e', 'eqid', 'eqname')
    )

    id = db.Column(db.Integer, primary_key=True)
    ksid = db.Column(db.Integer)
    eqid = db.Column(db.String(10), nullable=True)
    eqname = db.Column(db.String(10), nullable=True)
    maid = db.Column(db.String(255), nullable=True)
    lxfs = db.Column(db.String(255), nullable=True)
    wxdata = db.Column(db.Date, nullable=True)
    ren = db.Column(db.String(255), nullable=True)
    pj = db.Column(db.String(255), nullable=True)

    eqname1 = db.relationship('Eqname', primaryjoin='and_(Maininfo.eqid == Eqname.eqid, Maininfo.eqname == Eqname.eqname)', backref='maininfos')

    def __init__(self,ksid, eqid,eqname,maid,lxfs,wxdata,ren,pj):
        self.ksid = ksid
        self.eqid = eqid
        self.eqname = eqname
        self.maid = maid
        self.lxfs = lxfs
        self.wxdata = wxdata
        self.ren = ren
        self.pj = pj

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(UserMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    fullname = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=True)

    def __init__(self, username,password,fullname,email,phone,status):
        
        self.username = username
        self.password =password
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
    
class Keshi(db.Model):
    __tablename__ = 'keshi'

    id = db.Column(db.Integer, primary_key=True)
    kename = db.Column(db.String(255), nullable=True)

    def __init__(self, kename):
        
        self.kename = kename

    def save(self):
        db.session.add(self)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


