# Generated by Django 2.0.7 on 2020-07-21 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='版本号')),
                ('founder', models.CharField(blank=True, max_length=20, null=True, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('model_url', models.FileField(null=True, upload_to='model', verbose_name='车站模型路径')),
                ('version_des', models.TextField(blank=True, max_length=200, null=True, verbose_name='版本描述')),
            ],
            options={
                'db_table': 'model_version',
            },
        ),
        migrations.CreateModel(
            name='RePorts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reports_id', models.CharField(max_length=30, verbose_name='报告编号')),
                ('scheme_id', models.CharField(max_length=30, verbose_name='仿真方案id')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='选择开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='选择结束时间')),
                ('reports_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='报告存储目录（包括文件夹和报告名称）')),
            ],
            options={
                'db_table': 'reports',
            },
        ),
        migrations.CreateModel(
            name='StationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='图纸名称')),
                ('image_format', models.CharField(blank=True, max_length=10, null=True, verbose_name='图片格式')),
                ('image_url', models.ImageField(null=True, upload_to='station', verbose_name='车站图片路径')),
                ('founder', models.CharField(blank=True, max_length=20, null=True, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'station_image',
            },
        ),
        migrations.CreateModel(
            name='TrainLine',
            fields=[
                ('line_id', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='线路编号')),
                ('line_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='线路名称')),
            ],
            options={
                'db_table': 'train_line',
            },
        ),
        migrations.CreateModel(
            name='TrainScheme',
            fields=[
                ('scheme_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='仿真方案id')),
                ('station_id', models.CharField(blank=True, max_length=4, null=True, verbose_name='车站编码')),
                ('station_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='仿真车站名称')),
                ('scheme_type', models.CharField(blank=True, max_length=4, null=True, verbose_name='仿真方案类型')),
                ('scheme_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='方案名称')),
                ('creater', models.CharField(blank=True, max_length=50, null=True, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='方案创建时间')),
                ('scheme_desc', models.TextField(blank=True, null=True, verbose_name='方案描述')),
                ('driving_date', models.CharField(blank=True, max_length=12, null=True, verbose_name='行车选择日期')),
                ('driving_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='行车数据类型')),
                ('psflow_date', models.CharField(blank=True, max_length=12, null=True, verbose_name='客流选择日期')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='模拟车站的开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='模拟车站的结束时间')),
                ('ps_pare_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='乘客参数状态类型')),
                ('editer', models.CharField(blank=True, max_length=20, null=True, verbose_name='修改人')),
                ('edi_time', models.DateTimeField(auto_now=True, null=True, verbose_name='方案修改时间')),
                ('is_run', models.CharField(blank=True, max_length=5, null=True, verbose_name='是否仿真完成')),
                ('is_save', models.CharField(blank=True, max_length=5, null=True, verbose_name='仿真是否保存')),
            ],
            options={
                'db_table': 'train_scheme',
            },
        ),
        migrations.CreateModel(
            name='TrainStation',
            fields=[
                ('station_id', models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='车站编号')),
                ('station_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='车站名称')),
                ('des', models.TextField(blank=True, max_length=100, null=True, verbose_name='车站描述')),
                ('station_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='车站类型')),
                ('pf_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='站台类型')),
                ('passages_num', models.IntegerField(blank=True, null=True, verbose_name='出入口数')),
                ('station_pic', models.ImageField(blank=True, max_length=255, null=True, upload_to='station', verbose_name='车站图片路径')),
                ('current_image_name', models.CharField(blank=True, max_length=15, null=True, verbose_name='当前车站图片名称')),
                ('wo_peak_hours', models.CharField(blank=True, max_length=30, null=True, verbose_name='工作日高峰时段')),
                ('ho_peak_hours', models.CharField(blank=True, max_length=30, null=True, verbose_name='节假日高峰时段')),
                ('current_model_version', models.CharField(blank=True, max_length=10, null=True, verbose_name='当前版本')),
                ('model_version_create_time', models.CharField(blank=True, max_length=20, null=True, verbose_name='模型版本的上传时间')),
                ('line', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='station_info.TrainLine', verbose_name='线路编号')),
            ],
            options={
                'db_table': 'train_station',
            },
        ),
        migrations.CreateModel(
            name='TransStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=4, verbose_name='车站id')),
                ('line_id', models.CharField(max_length=2, verbose_name='线路名称')),
                ('station_code', models.CharField(max_length=10, verbose_name='车站编码')),
            ],
            options={
                'db_table': 'trans_station',
            },
        ),
        migrations.AddField(
            model_name='stationimage',
            name='station',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='station_images', to='station_info.TrainStation', verbose_name='车站图纸'),
        ),
        migrations.AddField(
            model_name='modelversion',
            name='station',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='model_versions', to='station_info.TrainStation', verbose_name='车站仿真模型版本'),
        ),
    ]