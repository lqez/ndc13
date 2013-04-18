# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'ndc_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'ndc', ['Tag'])

        # Adding model 'Room'
        db.create_table(u'ndc_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'ndc', ['Room'])

        # Adding model 'SessionDate'
        db.create_table(u'ndc_sessiondate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'ndc', ['SessionDate'])

        # Adding model 'SessionTime'
        db.create_table(u'ndc_sessiontime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('begin', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'ndc', ['SessionTime'])

        # Adding model 'Company'
        db.create_table(u'ndc_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'ndc', ['Company'])

        # Adding model 'Speaker'
        db.create_table(u'ndc_speaker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndc.Company'], null=True)),
        ))
        db.send_create_signal(u'ndc', ['Speaker'])

        # Adding model 'Session'
        db.create_table(u'ndc_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2000, null=True, blank=True)),
            ('slide_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndc.Room'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndc.SessionDate'])),
        ))
        db.send_create_signal(u'ndc', ['Session'])

        # Adding M2M table for field speakers on 'Session'
        db.create_table(u'ndc_session_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'ndc.session'], null=False)),
            ('speaker', models.ForeignKey(orm[u'ndc.speaker'], null=False))
        ))
        db.create_unique(u'ndc_session_speakers', ['session_id', 'speaker_id'])

        # Adding M2M table for field times on 'Session'
        db.create_table(u'ndc_session_times', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'ndc.session'], null=False)),
            ('sessiontime', models.ForeignKey(orm[u'ndc.sessiontime'], null=False))
        ))
        db.create_unique(u'ndc_session_times', ['session_id', 'sessiontime_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'ndc_tag')

        # Deleting model 'Room'
        db.delete_table(u'ndc_room')

        # Deleting model 'SessionDate'
        db.delete_table(u'ndc_sessiondate')

        # Deleting model 'SessionTime'
        db.delete_table(u'ndc_sessiontime')

        # Deleting model 'Company'
        db.delete_table(u'ndc_company')

        # Deleting model 'Speaker'
        db.delete_table(u'ndc_speaker')

        # Deleting model 'Session'
        db.delete_table(u'ndc_session')

        # Removing M2M table for field speakers on 'Session'
        db.delete_table('ndc_session_speakers')

        # Removing M2M table for field times on 'Session'
        db.delete_table('ndc_session_times')


    models = {
        u'ndc.company': {
            'Meta': {'object_name': 'Company'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'ndc.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ndc.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndc.SessionDate']"}),
            'desc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndc.Room']"}),
            'slide_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ndc.Speaker']", 'symmetrical': 'False'}),
            'times': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ndc.SessionTime']", 'symmetrical': 'False'})
        },
        u'ndc.sessiondate': {
            'Meta': {'object_name': 'SessionDate'},
            'day': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ndc.sessiontime': {
            'Meta': {'object_name': 'SessionTime'},
            'begin': ('django.db.models.fields.TimeField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ndc.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndc.Company']", 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'ndc.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ndc']
