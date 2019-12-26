#! /usr/bin/env python
#-*- coding: utf-8 -*-

import cgi, re, sys, os
from tools import utils

def remove_bug_err_id(error_id, status):

  PgConn   = utils.get_dbconn()
  PgCursor = PgConn.cursor()

  # find source
  PgCursor.execute("SELECT uuid,source,class FROM marker WHERE uuid_to_bigint(uuid) = %s", (error_id, ))
  source_id = None
  for res in PgCursor.fetchall():
      uuid = res["uuid"]
      source_id = res["source"]
      class_id = res["class"]

  if not source_id:
      return -1

  PgCursor.execute("DELETE FROM dynpoi_status WHERE uuid=%s", (uuid, ))

  PgCursor.execute("""INSERT INTO dynpoi_status
                        (source,class,elems,date,status,lat,lon,subtitle,uuid)
                      SELECT source,class,elems,NOW(),%s,
                             lat,lon,subtitle,uuid
                      FROM marker
                      WHERE uuid = %s
                      ON CONFLICT DO NOTHING""",
                   (status, uuid))

  PgCursor.execute("DELETE FROM marker WHERE uuid = %s", (uuid, ))
  PgCursor.execute("UPDATE dynpoi_class SET count = count - 1 WHERE source = %s AND class = %s;", (source_id, class_id))
  PgConn.commit()

  return 0


def remove_bug_uuid(uuid, status):

  PgConn   = utils.get_dbconn()
  PgCursor = PgConn.cursor()

  # find source
  PgCursor.execute("SELECT source,class FROM marker WHERE uuid = %s", (uuid, ))
  source_id = None
  for res in PgCursor.fetchall():
      source_id = res["source"]
      class_id = res["class"]

  if not source_id:
      return -1

  PgCursor.execute("DELETE FROM dynpoi_status WHERE uuid=%s", (uuid, ))

  PgCursor.execute("""INSERT INTO dynpoi_status
                        (source,class,elems,date,status,lat,lon,subtitle,uuid)
                      SELECT source,class,elems,NOW(),%s,
                             lat,lon,subtitle,uuid
                      FROM marker
                      WHERE uuid = %s
                      ON CONFLICT DO NOTHING""",
                   (status, uuid))

  PgCursor.execute("DELETE FROM marker WHERE uuid = %s", (uuid, ))
  PgCursor.execute("UPDATE dynpoi_class SET count = count - 1 WHERE source = %s AND class = %s;", (source_id, class_id))
  PgConn.commit()

  return 0
