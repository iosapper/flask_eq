from app import get_logger, get_config,db
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.models import Eqname,Eqinfo,Ininfo,Maininfo
from app.eqde.forms import EqNameForm,EqNameForms,IninfoForms,MaininfoForms
from werkzeug.utils import secure_filename
from . import eqde
import os
from flask_paginate import Pagination,get_page_parameter

logger = get_logger(__name__)



@eqde.route('/eqnamede/<ksid>', methods=['GET', 'POST'])
@login_required
def eqnamede(ksid):
    eqid = request.args.get('eqid')
    print(eqid)
    eqeqde = Eqinfo.query.filter(Eqinfo.eqid == eqid).first()
    eqeqce1TF = False
    eqeqce2TF = False
    eqeqce3TF = False
    eqeqce4TF = False
    eqeqce5TF = False
    try:
        os.remove(os.path.join("./app/static", eqeqde.eqce1file_url))
    except:
        flash('记录已删除，但税务登记证文件不存在')
    else:
        eqeqce1TF = True
    try:
        os.remove(os.path.join("./app/static", eqeqde.eqce2file_url))
    except:
        flash('记录已删除，但营业执照文件不存在')
    else:
        eqeqce2TF = True
    try:
        os.remove(os.path.join("./app/static", eqeqde.eqce3file_url))
    except:
        flash('记录已删除，但组织机构代码证文件不存在')
    else:
        eqeqce3TF = True
    try:
        os.remove(os.path.join("./app/static", eqeqde.eqce4file_url))
    except:
        flash('记录已删除，但经销商证件文件不存在')
    else:
        eqeqce4TF = True
    try:
        os.remove(os.path.join("./app/static", eqeqde.eqce5file_url))
    except:
        flash('记录已删除，但设备说明书文件不存在')
    else:
        eqeqce5TF = True
    db.session.delete(eqeqde)
    db.session.commit()
    eqinde = Ininfo.query.filter(Ininfo.eqid == eqid).all()
    eqeqce6TF = False
    try:
        for e in eqinde:
            try:
                os.remove(os.path.join("./app/static", e.smjfile_url))
            except:
                flash('记录已删除，但扫描件文件不存在')
            else:
                eqeqce6TF = True
            try:
                db.session.delete(e)
                db.session.commit()
            except:
                print("不存在")
    except:
        try:
            os.remove(os.path.join("./app/static", eqinde.smjfile_url))
        except:
            flash('记录已删除，但扫描件文件不存在')
        else:
            eqeqce6TF = True
        try:
            db.session.delete(eqinde)
            db.session.commit()
        except:
            print("不存在")
    eqmade = Maininfo.query.filter(Maininfo.eqid == eqid).all()
    try:
        for e in eqmade:
            try:
                db.session.delete(e)
                db.session.commit()
            except:
                print("不存在")
    except:
        try:
            db.session.delete(eqmade)
            db.session.commit()
        except:
            print("不存在")
    eqnade = Eqname.query.filter(Eqname.eqid == eqid).first()
    db.session.delete(eqnade)
    db.session.commit()
    if eqeqce1TF or eqeqce2TF or eqeqce3TF or eqeqce4TF or eqeqce5TF or eqeqce6TF:
        pass
    else:
        flash('删除成功')
    return redirect(url_for('eqname.eqnames',ksid=ksid))


@eqde.route('/ininfode/<ksid>', methods=['GET', 'POST'])
@login_required
def ininfode(ksid):
    eqid = request.args.get('eqid')
    prid = request.args.get('prid')
    inde = Ininfo.query.filter(Ininfo.prid == prid).first()
    smj = os.path.join("./app/static", inde.smjfile_url)
    try:
        os.remove(smj)
    except:
        flash('记录已删除，但文件不存在')
    else:
        flash('删除成功')
    db.session.delete(inde)
    db.session.commit()
    return redirect(url_for('eqname.ininfo',eqid=eqid,ksid=ksid))

@eqde.route('/maininfode/<ksid>', methods=['GET', 'POST'])
@login_required
def maininfode(ksid):
    eqid = request.args.get('eqid')
    maid = request.args.get('maid')
    made = Maininfo.query.filter(Maininfo.maid == maid).first()
    db.session.delete(made)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('eqname.maininfo',eqid=eqid,ksid=ksid))
