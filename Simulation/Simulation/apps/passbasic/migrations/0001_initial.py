# Generated by Django 2.0.7 on 2020-07-21 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquFacStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sta_type_id', models.CharField(max_length=2, verbose_name='状态类型编号')),
                ('sta_type_name', models.CharField(max_length=10, verbose_name='状态类型名称')),
            ],
            options={
                'db_table': 'equ_fac_status',
            },
        ),
        migrations.CreateModel(
            name='EsCsStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=4, verbose_name='车站代码')),
                ('ps_pare_type', models.CharField(max_length=10, verbose_name='乘客参数状态类型')),
                ('eq_id', models.CharField(max_length=20, verbose_name='设备编号')),
                ('loc', models.CharField(max_length=20, verbose_name='设备设施位置')),
                ('eq_status', models.CharField(max_length=10, verbose_name='设备设施状态')),
                ('equ_name', models.CharField(default='扶梯', max_length=6, verbose_name='设备名称')),
            ],
            options={
                'db_table': 'es_cs_status',
            },
        ),
        migrations.CreateModel(
            name='FenceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=4, verbose_name='车站代码')),
                ('ps_pare_type', models.CharField(max_length=10, verbose_name='乘客参数状态类型')),
                ('eq_id', models.CharField(max_length=20, verbose_name='设备编号')),
                ('loc', models.CharField(max_length=20, verbose_name='设备设施位置')),
                ('eq_status', models.CharField(max_length=10, verbose_name='设备设施状态')),
                ('equ_name', models.CharField(default='导流栏', max_length=6, verbose_name='设备名称')),
            ],
            options={
                'db_table': 'fence_status',
            },
        ),
        migrations.CreateModel(
            name='GateStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=4, verbose_name='车站代码')),
                ('ps_pare_type', models.CharField(max_length=10, verbose_name='乘客参数状态类型')),
                ('eq_id', models.CharField(max_length=20, verbose_name='设备编号')),
                ('loc', models.CharField(max_length=20, verbose_name='设备设施位置')),
                ('eq_status', models.CharField(max_length=10, verbose_name='设备设施状态')),
                ('equ_name', models.CharField(default='闸机', max_length=6, verbose_name='设备名称')),
            ],
            options={
                'db_table': 'gate_status',
            },
        ),
        migrations.CreateModel(
            name='GateWayStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=4, verbose_name='车站代码')),
                ('ps_pare_type', models.CharField(max_length=10, verbose_name='乘客参数状态类型')),
                ('eq_id', models.CharField(max_length=20, verbose_name='设备编号')),
                ('loc', models.CharField(max_length=20, verbose_name='设备设施位置')),
                ('eq_status', models.CharField(max_length=10, verbose_name='设备设施状态')),
                ('equ_name', models.CharField(default='出入口', max_length=6, verbose_name='设备名称')),
                ('orig_in_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='原始进站比例')),
                ('var_in_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='变化进站比例')),
                ('orig_out_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='原始出站比例')),
                ('var_out_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='变化出站比例')),
            ],
            options={
                'db_table': 'gate_way_status',
            },
        ),
        migrations.CreateModel(
            name='InOutRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(blank=True, max_length=4, null=True, verbose_name='车站编号')),
                ('ps_pare_type', models.CharField(max_length=20, verbose_name='乘客参数类型')),
                ('eq_id', models.CharField(max_length=20, verbose_name='出入口编号')),
                ('in_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='进站比例')),
                ('out_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='出站比例')),
            ],
            options={
                'db_table': 'inout_rate',
            },
        ),
        migrations.CreateModel(
            name='PsComp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=4, verbose_name='车站编号')),
                ('ps_pare_type', models.CharField(max_length=20, verbose_name='乘客参数类型')),
                ('male_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='男性比例')),
                ('female_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='女性比例')),
                ('personal_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='个体出行比例')),
                ('team_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='团体出行比例')),
                ('older_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='老年人比例')),
                ('adult_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='成年人比例')),
                ('child_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='儿童比例')),
                ('no_bag_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='无包比例')),
                ('small_bag_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='小包比例')),
                ('big_bag_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='大包比例')),
                ('mo_speed', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='男性老年人期望速度')),
                ('mo_space', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='男性老年人肩宽')),
                ('ma_speed', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='男性成年人期望速度')),
                ('ma_space', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='男性成年人肩宽')),
                ('mc_speed', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='男性未成年人期望速度')),
                ('mc_space', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='男性未成年人肩宽')),
                ('fo_speed', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='女性老年人期望速度')),
                ('fo_space', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='女性老年人肩宽')),
                ('fa_speed', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='女成年人期望速度')),
                ('fa_space', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='女性成年人肩宽')),
                ('fc_speed', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='女性未成年人期望速度')),
                ('fc_space', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='女性未成年人肩宽')),
            ],
            options={
                'db_table': 'ps_comp',
            },
        ),
        migrations.CreateModel(
            name='PsEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_transfer', models.CharField(blank=True, max_length=10, null=True, verbose_name='是否为换乘站')),
                ('station_id', models.CharField(blank=True, max_length=4, null=True, verbose_name='车站编号')),
                ('ps_pare_type', models.CharField(max_length=20, verbose_name='乘客参数类型')),
                ('tvm_tickets_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='自动售票机购票使用时间')),
                ('tvm_recharge_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='自动售票机充值使用时间')),
                ('bom_tickets_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='人工售票机购票使用时间')),
                ('bom_recharge_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='人工售票机充值使用时间')),
                ('sc_big_bag_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='大包安检时间')),
                ('sc_small_bag_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='小包安检时间')),
                ('sc_fast_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='快捷安检时间')),
                ('sc_fast_rate', models.IntegerField(verbose_name='快捷安检比例')),
                ('gate_normal_time', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='闸机正常使用时间')),
                ('gate_big_bag_time', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='闸机大包使用时间')),
                ('tvm_use_rate', models.IntegerField(blank=True, null=True, verbose_name='自动售票使用比例')),
                ('bom_use_rate', models.IntegerField(blank=True, null=True, verbose_name='人工售票机使用比例')),
                ('no_use_rate', models.IntegerField(blank=True, null=True, verbose_name='不适用设备的比例')),
                ('tvm_tickets_rate', models.IntegerField(verbose_name='自动售票机购票使用比例')),
                ('tvm_recharge_rate', models.IntegerField(verbose_name='自动售票机充值使用比例')),
                ('bom_tickets_rate', models.IntegerField(verbose_name='人工售票机购票使用比例')),
                ('bom_recharge_rate', models.IntegerField(verbose_name='人工售票机充值使用比例')),
            ],
            options={
                'db_table': 'ps_equipment',
            },
        ),
        migrations.CreateModel(
            name='PsFacilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_transfer', models.CharField(blank=True, max_length=10, null=True, verbose_name='是否为换乘站')),
                ('station_id', models.CharField(blank=True, max_length=4, null=True, verbose_name='车站编号')),
                ('ps_pare_type', models.CharField(max_length=20, verbose_name='乘客参数类型')),
                ('stup_design_cap', models.IntegerField(verbose_name='上行楼梯设计通过能力')),
                ('stdown_design_cap', models.IntegerField(verbose_name='下行楼梯设计通过能力')),
                ('stmix_design_cap', models.IntegerField(verbose_name='混行楼梯设计通过能力')),
                ('esup_design_cap', models.IntegerField(verbose_name='上行扶梯设计通过能力')),
                ('esdown_design_cap', models.IntegerField(verbose_name='下行扶梯设计通过能力')),
                ('gasin_design_cap', models.IntegerField(verbose_name='闸机单向通道设计通过能力')),
                ('gadou_design_cap', models.IntegerField(verbose_name='闸机双向通道设计通过能力')),
                ('thsin_design_cap', models.IntegerField(verbose_name='换乘单向通道设计通过能力')),
                ('thdou_design_cap', models.IntegerField(verbose_name='换乘双向通道设计通过能力')),
                ('sc_design_cap', models.IntegerField(verbose_name='安检机设计通过能力')),
                ('la_design_cap', models.IntegerField(verbose_name='水平步梯设计通过能力')),
                ('el_design_cap', models.IntegerField(verbose_name='电梯设计通过能力')),
            ],
            options={
                'db_table': 'ps_facilities',
            },
        ),
        migrations.CreateModel(
            name='TrainPartRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(blank=True, max_length=4, null=True, verbose_name='车站编号')),
                ('ps_pare_type', models.CharField(max_length=20, verbose_name='乘客参数类型')),
                ('line_name', models.CharField(max_length=50, verbose_name='线路名称')),
                ('eq_id', models.CharField(max_length=20, verbose_name='车厢编号')),
                ('direct_id', models.CharField(max_length=5, verbose_name='站台方向')),
                ('board_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='列车车厢上车比例')),
                ('getoff_rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='列车车厢下车比例')),
            ],
            options={
                'db_table': 'train_part_rate',
            },
        ),
    ]
