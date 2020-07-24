from app import get_logger, get_config,db
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.models import Eqname,Eqinfo,Keshi,Ininfo,Maininfo
from app.eqname.forms import EqNameForm,EqNameForms,KeshiForms,IninfoForms,MaininfoForms
from werkzeug.utils import secure_filename
from . import eqname
import os
from flask_paginate import Pagination,get_page_parameter

logger = get_logger(__name__)


# 根目录跳转
@eqname.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('eqname.index'))


# 首页
@eqname.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        kename = request.form.get('kename')
        if Keshi.query.filter(Keshi.kename == kename).first():
            flash("设备编号重复")
        else:
            eqnamesave = Keshi(kename)
            eqnamesave.save()
            flash('保存成功')
    Keshiform = Keshi.query.filter().all()
    return render_template('index.html', Keshiform = Keshiform ,form = KeshiForms(),current_user=current_user)



@eqname.route('/eqnames/<ksid>', methods=['GET', 'POST'])
@login_required
def eqnames(ksid):
    if request.method == 'POST':
                eqid = request.form.get('eqid')
                eqname = request.form.get('eqname')
                if Eqname.query.filter(Eqname.eqid == eqid).first():
                    flash("设备编号重复")
                else:
                    eqnamesave = Eqname(ksid,eqid,eqname)
                    eqnamesave.save()
                    flash('保存成功')
    PER_PAGE = 10
    total = Eqname.query.filter(Eqname.ksid==ksid).count()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    models = Eqname.query.filter(Eqname.ksid==ksid).slice(start,end)
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    return render_template('eqname.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,forms=models,pagination=pagination, form=EqNameForm(), current_user=current_user)


@eqname.route('/img/<ksid>/<eqid>/', methods=['GET', 'POST'])
@login_required
def img(ksid,eqid):
    file_url = request.args.get('file_url')
    eqname = request.args.get('eqname')
    byto = request.args.get('byto')
    print(byto)
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    return render_template('img.html',eqname=eqname,ksid=ksid,ksname = ksname,eqid = eqid,Keshiform = Keshiform ,byto = byto ,current_user=current_user)


@eqname.route('/eqinfo/<ksid>', methods=['GET', 'POST'])
@login_required
def eqinfo(ksid):
    eqid = request.args.get('eqid')
    g = Eqinfo.query.filter(Eqinfo.eqid == eqid).first()
    total = Eqinfo.query.filter(Eqinfo.eqid==eqid)
    centent=total.all()[0]
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    if request.method == 'POST':
        eqprdata = request.form.get('eqprdata')
        equsedata = request.form.get('equsedata')
        eqce1TF = False
        eqce2TF = False
        eqce3TF = False
        eqce4TF = False
        eqce5TF = False

        eqce1 = request.files['eqce1']
        eqce1filename = secure_filename(eqce1.filename)  # 文件名安全
        if Eqinfo.query.filter(Eqinfo.eqce1filename == eqce1filename).first():
            flash("税务登记证名称重复")
            eqce1TF = True
        eqce1.save(os.path.join("./app/static/to/eqce1", eqce1filename))
        eqce1file_url = (os.path.join("to/eqce1", eqce1filename))

        eqce2 = request.files['eqce2']
        eqce2filename = secure_filename(eqce2.filename)  # 文件名安全
        eqce2.save(os.path.join("./app/static/to/eqce2", eqce2filename))
        eqce2file_url = (os.path.join("to/eqce2", eqce2filename))
        if Eqinfo.query.filter(Eqinfo.eqce2filename == eqce2filename).first():
            flash("营业执照名称重复")
            eqce2TF = True

        eqce3 = request.files['eqce3']
        eqce3filename = secure_filename(eqce3.filename)  # 文件名安全
        eqce3.save(os.path.join("./app/static/to/eqce3", eqce3filename))
        eqce3file_url = (os.path.join("to/eqce3", eqce3filename))
        if Eqinfo.query.filter(Eqinfo.eqce3filename == eqce3filename).first():
            flash("组织机构代码证名称重复")
            eqce3TF = True

        eqce4 = request.files['eqce4']
        eqce4filename = secure_filename(eqce4.filename)  # 文件名安全
        eqce4.save(os.path.join("./app/static/to/eqce4", eqce4filename))
        eqce4file_url = (os.path.join("to/eqce5", eqce4filename))
        if Eqinfo.query.filter(Eqinfo.eqce4filename == eqce4filename).first():
            flash("经销商证件名称重复")
            eqce4TF = True

        eqce5 = request.files['eqce5']
        eqce5filename = secure_filename(eqce5.filename)  # 文件名安全
        if Eqinfo.query.filter(Eqinfo.eqce5filename == eqce5filename).first():
            flash("设备说明书名称重复")
            eqce5TF = True
        eqce5.save(os.path.join("./app/static/to/eqce5", eqce5filename))
        eqce5file_url = (os.path.join("to/eqce5", eqce5filename))
        if eqce1TF or eqce2TF or eqce3TF or eqce4TF or eqce5TF:
            flash("添加失败")
            return render_template('eqinfo.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,centent=centent,form=EqNameForms(),current_user=current_user)
        else:
            g.eqprdata = eqprdata
            db.session.commit()
            g.equsedata = equsedata
            db.session.commit()
            g.eqce1filename = eqce1filename
            db.session.commit()
            g.eqce1file_url = eqce1file_url
            db.session.commit()
            g.eqce2filename = eqce2filename
            db.session.commit()
            g.eqce2file_url = eqce2file_url
            db.session.commit()
            g.eqce3filename = eqce3filename
            db.session.commit()
            g.eqce3file_url = eqce3file_url
            db.session.commit()
            g.eqce4filename = eqce4filename
            db.session.commit()
            g.eqce4file_url = eqce4file_url
            db.session.commit()
            g.eqce5filename = eqce5filename
            db.session.commit()
            g.eqce5file_url = eqce5file_url
            db.session.commit()
            flash("添加成功")
            return render_template('eqinfos.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,centent=centent,current_user=current_user)
    else:
        if g:
            if total.all()[0].eqprdata ==None and total.all()[0].equsedata==None:
                return render_template('eqinfo.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,centent=centent,form=EqNameForms(),current_user=current_user)
            else:    
                return render_template('eqinfos.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,centent=centent,current_user=current_user)
        else:
            flash("设备资料不存在，请删除设备后重试")
            return redirect(url_for('eqname.eqnames',ksid=ksid))

@eqname.route('/ininfo/<ksid>', methods=['GET', 'POST'])
@login_required
def ininfo(ksid):
    eqid = request.args.get('eqid')
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    eqname = Eqname.query.filter(Eqname.eqid == eqid).first().eqname
    PER_PAGE = 10
    total = Ininfo.query.filter(Ininfo.eqid==eqid).count()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    models = Ininfo.query.filter(Ininfo.eqid==eqid).slice(start,end)
    if request.method == 'POST':
        prid = request.form.get('prid')
        smj = request.files['smj']
        smj = request.files['smj']
        smjTF = False
        pridTF = False
        smjfilename = secure_filename(smj.filename)  # 文件名安全
        smj.save(os.path.join("./app/static/to/eqce6", smjfilename))
        smjfile_url = (os.path.join("to/eqce6", smjfilename))
        if Ininfo.query.filter(Ininfo.prid == prid).first():
            flash("检验项目编号重复")
            pridTF=True
        if Ininfo.query.filter(Ininfo.smjfilename == smjfilename).first():
            flash("税务登记证名称重复")
            smjTF=True
        if pridTF or smjTF :
            return render_template('ininfo.html',eqid = eqid,ksname = ksname,eqname = eqname,ksid=ksid,forms=models,pagination=pagination,Keshiform = Keshiform ,form = IninfoForms(),current_user=current_user)
        else:
                ininfosave = Ininfo(ksid,eqid,eqname,prid,smjfilename,smjfile_url)
                ininfosave.save()
                flash('保存成功')

    return render_template('ininfo.html',eqid = eqid,ksname = ksname,eqname = eqname,ksid=ksid,forms=models,pagination=pagination,Keshiform = Keshiform ,form = IninfoForms(),current_user=current_user)


@eqname.route('/maininfo/<ksid>', methods=['GET', 'POST'])
@login_required
def maininfo(ksid):
    eqid = request.args.get('eqid')
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    eqname = Eqname.query.filter(Eqname.eqid == eqid).first().eqname
    PER_PAGE = 10
    total = Maininfo.query.filter(Maininfo.eqid==eqid).count()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    models = Maininfo.query.filter(Maininfo.eqid==eqid).slice(start,end)
    if request.method == 'POST':
        maid = request.form.get('maid')
        lxfs = request.form.get('lxfs')
        wxdata = request.form.get('wxdata')
        ren = request.form.get('ren')
        pj = request.form.get('pj')
        if Maininfo.query.filter(Maininfo.maid == maid).first():
            flash("维修记录编号重复")
            return render_template('maininfo.html',eqid = eqid,ksname = ksname,eqname = eqname,ksid=ksid,forms=models,pagination=pagination,Keshiform = Keshiform ,form = MaininfoForms(),current_user=current_user)
        else:
                ininfosave = Maininfo(ksid,eqid,eqname,maid,lxfs,wxdata,ren,pj)
                ininfosave.save()
                flash('保存成功')

    return render_template('maininfo.html',eqid = eqid,ksname = ksname,eqname = eqname,ksid=ksid,forms=models,pagination=pagination,Keshiform = Keshiform ,form = MaininfoForms(),current_user=current_user)
