from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField,FileField,DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_wtf.file import FileRequired, FileAllowed


class EqNameForm(FlaskForm):
    eqid = StringField('设备编号', validators=[DataRequired(), Length(1, 64), ])
    eqname = StringField('设备名', validators=[DataRequired()])
    submit = SubmitField('新增设备')

class EqNameForms(FlaskForm):
    eqid = StringField('设备编号', validators=[DataRequired(), Length(1, 10)])
    eqname = StringField('设备名', validators=[DataRequired(), Length(1, 10)])
    eqprdata = DateField("设备生产日期", validators=[DataRequired()])
    equsedata = DateField("设备投用日期", validators=[DataRequired()])
    eqce1 = FileField('税务登记证',validators=[FileAllowed(['jpg', 'png', 'gif']),DataRequired()])
    eqce2 = FileField('营业执照',validators=[FileAllowed(['jpg', 'png', 'gif']),DataRequired()])
    eqce3 = FileField('组织机构代码证',validators=[FileAllowed(['jpg', 'png', 'gif']),DataRequired()])
    eqce4 = FileField('经销商证件',validators=[FileAllowed(['jpg', 'png', 'gif']),DataRequired()])
    eqce5 = FileField('设备说明书',validators=[FileAllowed(['jpg', 'png', 'gif']),DataRequired()])
    submit = SubmitField('提交')

class IninfoForms(FlaskForm):
    prid = StringField('检验项目编号', validators=[DataRequired(), Length(1, 10)])
    smj = FileField('设备说明书',validators=[FileAllowed(['jpg', 'png', 'gif']),DataRequired()])
    submit = SubmitField('添加检验项目')

class MaininfoForms(FlaskForm):
    maid = StringField('维修记录编号', validators=[DataRequired(), Length(1, 10)])
    lxfs = StringField('联系方式', validators=[DataRequired(), Length(1, 10)])
    wxdata = DateField("维修维保项目日期", validators=[DataRequired()])
    ren = StringField('维修维保项目人员', validators=[DataRequired(), Length(1, 10)])
    pj = StringField('更换配件及价格记录', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField('添加维修记录')