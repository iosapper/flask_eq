from app import get_logger, get_config,db
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.models import Eqname,Eqinfo,Ininfo,Maininfo,Keshi
from app.equp.forms import EqNameUpForm,MaininfoUpForm,IninfoUpForm,EqinfoUpForm
from werkzeug.utils import secure_filename
from . import equp
import datetime
import os
from flask_paginate import Pagination,get_page_parameter

logger = get_logger(__name__)



@equp.route('/eqnameup/<ksid>', methods=['GET', 'POST'])
@login_required
def eqnameup(ksid):
    PER_PAGE = 10
    total = Eqname.query.filter(Eqname.ksid==ksid).count()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    models = Eqname.query.filter(Eqname.ksid==ksid).all()
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    if request.method == 'POST':
        oldeqid = request.form.get('oldeqid')
        eqid = request.form.get('eqid')
        eqname = request.form.get('eqname')
        equp = Eqname.query.filter(Eqname.eqid==oldeqid).first()
        oldeqname = equp.eqname
        if oldeqname != eqname:
            equp.eqname = eqname
            db.session.commit()
        if oldeqid != eqid:
            equp.eqid = eqid
            db.session.commit()
        flash("更新成功")
    return render_template('eqnameup.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,form = EqNameUpForm(), forms=models, current_user=current_user)

@equp.route('/eqmainup/<ksid>', methods=['GET', 'POST'])
@login_required
def eqmainup(ksid):


    if request.method == 'POST':
        oldmaid = request.form.get('oldmaid')
        maid = request.form.get('maid')
        lxfs = request.form.get('lxfs')
        wxdata = request.form.get('wxdata')
        wxdatadata = datetime.datetime.strptime(wxdata,'%Y-%m-%d').date()
        ren = request.form.get('ren')
        pj = request.form.get('pj')
        eqmaup = Maininfo.query.filter(Maininfo.maid==oldmaid).first()
        oldmaid = eqmaup.maid
        oldlxfs = eqmaup.lxfs
        oldwxdata = eqmaup.wxdata
        
        oldren = eqmaup.ren
        oldpj = eqmaup.pj
        if oldmaid != maid:
            eqmaup.maid = maid
            db.session.commit()
            flash("维修记录编号更新成功")
        if oldlxfs != lxfs:
            eqmaup.lxfs = lxfs
            db.session.commit()
            flash("联系方式更新成功")
        if oldwxdata != wxdatadata:
            eqmaup.wxdata = wxdata
            db.session.commit()
            flash("维修维保项目日期更新成功")
        if oldren != ren:
            eqmaup.ren = ren
            db.session.commit()
            flash("维修维保项目人员更新成功")
        if oldpj != pj:
            eqmaup.pj = pj
            db.session.commit()
            flash("更换配件及价格记录更新成功")
    eqid = request.args.get('eqid')
    PER_PAGE = 10
    total = Maininfo.query.filter(Maininfo.eqid==eqid).count()
    print(eqid)
    print(total)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    models = Maininfo.query.filter(Maininfo.eqid==eqid).slice(start,end)
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    return render_template('maininfoup.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,form = MaininfoUpForm(), forms=models,pagination=pagination, current_user=current_user)

@equp.route('/eqinup/<ksid>', methods=['GET', 'POST'])
@login_required
def eqinup(ksid):
    if request.method == 'POST':
        oldprid = request.form.get('oldprid')
        prid = request.form.get('prid')
        smj = request.files['smj']
        eqinup = Ininfo.query.filter(Ininfo.prid==oldprid).first()
        if smj:
            smjfilename = secure_filename(smj.filename)  # 文件名安全
            if Ininfo.query.filter(Ininfo.smjfilename == smjfilename).first():
                flash("扫描件名称重复")
            else:
                try:
                    os.remove(os.path.join("./app/static", eqinup.smjfile_url))
                except:
                    flash('记录已更新，但原营业执照不存在')
                smj.save(os.path.join("./app/static/to/eqce6", smjfilename))
                smjfile_url = (os.path.join("to/eqce6", smjfilename))
                eqinup.smjfilename = smjfilename
                db.session.commit()
                eqinup.smjfile_url = smjfile_url
                db.session.commit()
                flash("扫描件更新成功")
        else:
            print("smj不存在")
    eqid = request.args.get('eqid')
    PER_PAGE = 10
    total = Ininfo.query.filter(Ininfo.eqid==eqid).count()
    print(eqid)
    print(total)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    models = Ininfo.query.filter(Ininfo.eqid==eqid).slice(start,end)
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    return render_template('ininfoup.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,form = IninfoUpForm(), forms=models,pagination=pagination, current_user=current_user)

@equp.route('/eqinfoup/<ksid>', methods=['GET', 'POST'])
@login_required
def eqinfoup(ksid):
    eqid = request.args.get('eqid')
    g = Eqinfo.query.filter(Eqinfo.eqid == eqid).first()
    total = Eqinfo.query.filter(Eqinfo.eqid==eqid)
    centent=total.all()[0]
    Keshiform = Keshi.query.filter().all()
    ksname = Keshi.query.filter(Keshi.id == ksid).first().kename
    if request.method == 'POST':
        eqprdata = request.form.get('eqprdata')
        eqprdatadata = datetime.datetime.strptime(eqprdata,'%Y-%m-%d').date()
        equsedata = request.form.get('equsedata')
        equsedatadata = datetime.datetime.strptime(equsedata,'%Y-%m-%d').date()

        eqinup = Eqinfo.query.filter(Eqinfo.eqid==eqid).first()
        oldeqprdata = eqinup.eqprdata
        oldequsedata = eqinup.equsedata
        oldeqce1filename = eqinup.eqce1filename
        oldeqce1file_url = eqinup.eqce1file_url
        oldeqce2filename = eqinup.eqce2filename
        oldeqce2file_url = eqinup.eqce2file_url
        oldeqce3filename = eqinup.eqce3filename
        oldeqce3file_url = eqinup.eqce3file_url
        oldeqce4filename = eqinup.eqce4filename
        oldeqce4file_url = eqinup.eqce4file_url
        oldeqce5filename = eqinup.eqce5filename
        oldeqce5file_url = eqinup.eqce5file_url
        
        if oldeqprdata != eqprdatadata:
            eqinup.eqprdata = eqprdata
            db.session.commit()
            flash("设备生产日期更新成功")
        if oldequsedata != equsedatadata:
            eqinup.equsedata = equsedata
            db.session.commit()
            flash("设备投用日期更新成功")

        eqce1 = request.files['eqce1']
        if eqce1:
            eqce1filename = secure_filename(eqce1.filename)  # 文件名安全
            if Eqinfo.query.filter(Eqinfo.eqce1filename == eqce1filename).first():
                flash("税务登记证名称重复")
            else:
                try:
                    os.remove(os.path.join("./app/static", eqinup.eqce1file_url))
                except:
                    flash('记录已更新，但原税务登记证不存在')
                eqce1.save(os.path.join("./app/static/to/eqce1", eqce1filename))
                eqce1file_url = (os.path.join("to/eqce1", eqce1filename))
                eqinup.eqce1filename = eqce1filename
                db.session.commit()
                eqinup.eqce1file_url = eqce1file_url
                db.session.commit()
                flash("税务登记证更新成功")
       
        eqce2 = request.files['eqce2']
        if eqce2:
            eqce2filename = secure_filename(eqce2.filename)  # 文件名安全
            if Eqinfo.query.filter(Eqinfo.eqce2filename == eqce2filename).first():
                flash("营业执照名称重复")
            else:
                try:
                    os.remove(os.path.join("./app/static", eqinup.eqce2file_url))
                except:
                    flash('记录已更新，但原营业执照不存在')
                eqce2.save(os.path.join("./app/static/to/eqce2", eqce2filename))
                eqce2file_url = (os.path.join("to/eqce2", eqce2filename))
                eqinup.eqce2filename = eqce2filename
                db.session.commit()
                eqinup.eqce2file_url = eqce2file_url
                db.session.commit()
                flash("营业执照更新成功")

        eqce3 = request.files['eqce3']
        if eqce3:
            eqce3filename = secure_filename(eqce3.filename)  # 文件名安全
            if Eqinfo.query.filter(Eqinfo.eqce3filename == eqce3filename).first():
                flash("组织机构代码证名称重复")
            else:
                try:
                    os.remove(os.path.join("./app/static", eqinup.eqce3file_url))
                except:
                    flash('记录已更新，但原组织机构代码证不存在')
                eqce3.save(os.path.join("./app/static/to/eqce3", eqce3filename))
                eqce3file_url = (os.path.join("to/eqce3", eqce3filename))
                eqinup.eqce3filename = eqce3filename
                db.session.commit()
                eqinup.eqce3file_url = eqce3file_url
                db.session.commit()
                flash("组织机构代码证更新成功")

        eqce4 = request.files['eqce4']
        if eqce4:
            eqce4filename = secure_filename(eqce4.filename)  # 文件名安全
            if Eqinfo.query.filter(Eqinfo.eqce4filename == eqce4filename).first():
                flash("经销商证件名称重复")
            else:
                try:
                    os.remove(os.path.join("./app/static", eqinup.eqce1file_url))
                except:
                    flash('记录已更新，但原经销商证件不存在')
                eqce4.save(os.path.join("./app/static/to/eqce4", eqce4filename))
                eqce4file_url = (os.path.join("to/eqce4", eqce4filename))
                eqinup.eqce4filename = eqce4filename
                db.session.commit()
                eqinup.eqce4file_url = eqce4file_url
                db.session.commit()
                flash("经销商证件更新成功")

        eqce5 = request.files['eqce5']
        if eqce5:
            eqce5filename = secure_filename(eqce5.filename)  # 文件名安全
            if Eqinfo.query.filter(Eqinfo.eqce5filename == eqce5filename).first():
                flash("设备说明书名称重复")
            else:
                try:
                    os.remove(os.path.join("./app/static", eqinup.eqce5file_url))
                except:
                    flash('记录已更新，但原设备说明书不存在')
                eqce5.save(os.path.join("./app/static/to/eqce5", eqce5filename))
                eqce5file_url = (os.path.join("to/eqce5", eqce5filename))
                eqinup.eqce5filename = eqce5filename
                db.session.commit()
                eqinup.eqce5file_url = eqce5file_url
                db.session.commit()
                flash("设备说明书更新成功")
        return render_template('eqinfoup.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,centent=centent,form=EqinfoUpForm(),current_user=current_user)
    else:
        if g:
            return render_template('eqinfoup.html',ksid=ksid,ksname = ksname,Keshiform = Keshiform ,centent=centent,form=EqinfoUpForm(),current_user=current_user)
        else:
            flash("设备资料不存在，请删除设备后重试")
            return redirect(url_for('equp.eqmainup',ksid=ksid))


