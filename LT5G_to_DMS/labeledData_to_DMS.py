
import json

class LabelProperties(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class LabelToolToDMSConverter(object):

    def __init__(self, lt5_json_fname):
        with open(lt5_json_fname) as data_file:
            self.lt5_json_obj = json.load(data_file)
        self.project = ''
        self.func = ''

        self.generate_ldroi_file()
        self.generate_ldss_file()

    def generate_ldroi_file(self):
        # Recording name should be the name of the file
        rec_name = self.lt5_json_obj['Sequence'][0]['DeviceCommonData']['Name']
        # Define the file name, Project and function information not included
        dms_ldroi_json_fname = 'LDROI_' + rec_name + '.json'

        # Gather all the track IDs
        all_anno_elmnts_lst = self.lt5_json_obj['Sequence'][0]['DeviceData'][0]['ChannelData'][0]['AnnotatedElements']
        track_ids = [evry_anno_elem['FrameAnnoElements'][0]['Trackid'] for evry_anno_elem in all_anno_elmnts_lst]
        # Get unique track IDs, then iterate through every track ID same/different updating the attributes
        # print "track_ids ::", track_ids
        track_ids = list(set(track_ids))
        # print "track_ids ::", track_ids

        dms_ldroi_json_obj = {}
        ldroi_attrib_dict = {}
        ech_trk_dict = {}
        for evry_trackid in track_ids:
            # ech_trackid_dict = self.generate_ech_trackid_dict(all_anno_elmnts_lst)
            # Iterate through every anno element
            # sampl_lst = []
            for ech_anno_element in all_anno_elmnts_lst:
                # print "ech_anno_element ::", ech_anno_element
                # Assign the project and function
                category = ech_anno_element['FrameAnnoElements'][0]['category']
                if '_' not in category:
                    self.project, self.func = category,  category
                else:
                    self.project, self.func = category.split('_')
                # Get the LDROI attributes, prepare a dictionary and assign their respective values
                ldroi_attrbs_dict = ech_anno_element['FrameAnnoElements'][0]['attributes']
                trackid_iter = ech_anno_element['FrameAnnoElements'][0]['Trackid']
                # print "trackid_iter >>", trackid_iter
                if evry_trackid == trackid_iter:
                    # ldroi_attrib_dict = {}
                    # print "ech_anno_element>>", ech_anno_element["TimeStamp"]
                    if "Trackid" in dms_ldroi_json_obj:
                        if trackid_iter in dms_ldroi_json_obj['Trackid'].keys():
                            tmstamp_lst = dms_ldroi_json_obj['Trackid'][trackid_iter]["TimeStamp"]
                            # Keys of the attribute
                            ldr_attribs_lst = dms_ldroi_json_obj['Trackid'][trackid_iter].keys()
                            ldr_attribs_lst.remove("TimeStamp")
                            # print "ldr_attribs_lst :>", ldr_attribs_lst
                            # break
                            if tmstamp_lst is not None:
                                tmstamp_lst.append(ech_anno_element["TimeStamp"])
                                # print ">>>", tmstamp_lst

                            for evry_ldr_attrib in ldr_attribs_lst:
                                # print "evry_ldr_attrib ::", evry_ldr_attrib
                                if dms_ldroi_json_obj['Trackid'][trackid_iter][evry_ldr_attrib] is not None:
                                    ldroi_attrib_appnd = dms_ldroi_json_obj['Trackid'][trackid_iter][evry_ldr_attrib]
                                    # print ">>>", ldroi_attrib_appnd
                                    ldroi_attrib_appnd.append(ldroi_attrbs_dict[evry_ldr_attrib])
                                    # dms_ldroi_json_obj['Trackid'][trackid_iter][evry_ldr_attrib] = ldroi_attrib_appnd
                                    ldroi_attrib_dict[str(evry_ldr_attrib)] = ldroi_attrib_appnd
                        # else:
                        #     tmstamp = [ech_anno_element["TimeStamp"]]
                        #     for evry_ldroi_attrib in ldroi_attrbs_dict:
                        #         ldroi_attrib_dict[str(evry_ldroi_attrib)] = [ldroi_attrbs_dict[evry_ldroi_attrib]]

                    else:
                        print "{{{"
                        # dms_ldroi_json_obj['Trackid']["TimeStamp"] = [ech_anno_element["TimeStamp"]]
                        # Assigning each attribute for the first time during initialization
                        tmstamp = [ech_anno_element["TimeStamp"]]
                        for evry_ldroi_attrib in ldroi_attrbs_dict:
                            ldroi_attrib_dict[str(evry_ldroi_attrib)] = [ldroi_attrbs_dict[evry_ldroi_attrib]]

                    ldroi_attrib_dict["TimeStamp"] = tmstamp
                    # print "category ::", self.project, self.func

                    ech_trk_dict.update({evry_trackid: ldroi_attrib_dict})
                    # print "ldroi_attrib_dict ::", ldroi_attrib_dict.__dict__
                    trackId_info_dict = ech_trk_dict
                    dms_ldroi_json_obj['FUNCTION'] = self.func
                    dms_ldroi_json_obj['FAMILY'] = self.project
                    dms_ldroi_json_obj['RecIdFileName'] = rec_name
                    dms_ldroi_json_obj['Trackid'] = trackId_info_dict


        with open(r'Output/' + dms_ldroi_json_fname, 'w+') as outfile:
            json.dump(dms_ldroi_json_obj, outfile, indent=4)

    def generate_ldss_file(self):
        # Recording name should be the name of the file
        rec_name = self.lt5_json_obj['Sequence'][0]['DeviceCommonData']['Name']
        # Define the file name, Project and function information not included
        dms_ldss_json_fname = 'LDSS_' + rec_name + '.json'

        # Gather all the track IDs
        all_info_elmnts_dict = self.lt5_json_obj['Sequence'][0]['DeviceData'][0]['InformationElements']

        # Get the file name, project and function
        first_anno_elem = self.lt5_json_obj['Sequence'][0]['DeviceData'][0]['ChannelData'][0]['AnnotatedElements'][0]
        category = first_anno_elem['FrameAnnoElements'][0]['category']
        if '_' not in category:
            self.project, self.func = category, category
        else:
            self.project, self.func = category.split('_')

        dms_ldss_json_obj = {}

        dms_ldss_json_obj['FUNCTION'] = self.func
        dms_ldss_json_obj['FAMILY'] = self.project
        dms_ldss_json_obj['RecIdFileName'] = rec_name

        # print "all_info_elmnts_dict ::", all_info_elmnts_dict
        # Structurize the entire skeleton for LDSS
        info_elems_lst = all_info_elmnts_dict.keys()
        # Mandatory keys that needs to be present
        # mandatory_attr_keys = ['LDSS_STOP_CYCLE_COUNTER']
        info_elem_dub_dict = {}
        for ech_info_elem in info_elems_lst:
            info_elem_dub_dict[ech_info_elem] = {}
        # Remove start and stop time stamp from the main dictionary
        info_elems_mod_lst = [e for e in info_elems_lst if e not in ('FrameMtLDSSTimeStampStart', 'FrameMtLDSSTimeStampStop')]
        for ech_info_elem in info_elems_mod_lst:
            # only have that key which has the same parent key
            info_elem_dub_dict = {evry_key_dict: val for evry_key_dict, val in info_elem_dub_dict.iteritems()
                                  if evry_key_dict == ech_info_elem}
            print "info_elem_dub_dict ::", info_elem_dub_dict
            dms_ldss_json_obj[ech_info_elem] = info_elem_dub_dict

        # Add data to each element, iterate through the LDSS file object
        # for evry_lt5_attr_dict in all_info_elmnts_dict:
        #     print evry_lt5_attr_dict
        for key_attr, ech_attr_vals_lst in all_info_elmnts_dict.iteritems():
            # Compare each LT5 labeled data attr with DMS attributes

            for key_dms_attr, ech_dms_ldss_attr in dms_ldss_json_obj.iteritems():
                if key_attr == key_dms_attr:
                    # Extract the timestamp range which has value
                    # print "key_attr ::", key_attr
                    val_lst = []
                    start_timestamp_lst = []
                    stop_timestamp_lst = []
                    for evry_ldss_tmstamp_dict in ech_attr_vals_lst:
                        # print "evry_ldss_tmstamp_dict >>", evry_ldss_tmstamp_dict
                        if evry_ldss_tmstamp_dict['value'] is not None:
                            val_lst.append(evry_ldss_tmstamp_dict['value'])
                            print "ech_dms_ldss_attr >", ech_dms_ldss_attr
                            ech_dms_ldss_attr[key_attr] = val_lst
                            start_timestamp_lst.append(evry_ldss_tmstamp_dict['start'])
                            print "start_timestamp_lst ::", start_timestamp_lst
                            ech_dms_ldss_attr['FrameMtLDSSTimeStampStart'] = start_timestamp_lst
                            stop_timestamp_lst.append(evry_ldss_tmstamp_dict['end'])
                            ech_dms_ldss_attr['FrameMtLDSSTimeStampStop'] = stop_timestamp_lst
                # break
        with open(r'Output/' + dms_ldss_json_fname, 'w+') as outfile:
            json.dump(dms_ldss_json_obj, outfile, indent=4)


if __name__ == '__main__':
    lt5_json_fname = r'2018081307340912110_LabelData.json'
    # lt5_json_fname = r'D:/LabelData_Y.json'
    LabelToolToDMSConverter(lt5_json_fname)
