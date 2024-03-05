#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from static.vuln_notify import vuln_found_notify
import requests

class analyze_cdn:
    """
    Cloudflare:
        X-Forwarded-Proto: http => 301/302/303 + CF-Cache-Status: HIT
    #TODO
    """

    def get_cdn(self, req_main, url, s):
        """
        Check what is the reverse proxy/WAF/cached server... and test based on the result
        """
        print("\033[36m ├ CDN analyse\033[0m")
        cdns = {
            "Cloudflare": ["cf-ray", "cloudflare", "cf-cache-status", "cf-ray"],
            # "CacheFly": "",
            # "Fastly": "",
        }
        for c in cdns:
            for v in cdns[c]:
                # case insensivity check
                lower_case_headers = {k.lower(): v.lower() for k, v in req_main.headers.items()}
                if v.lower() in req_main.text.lower() or v.lower() in lower_case_headers:
                    return c


    def Cloudflare(self, url, s):
        print("\033[36m --├ Cloudflare\033[0m")
        headers = {"X-Forwarded-Proto": "nohttps"}
        cf_loop = s.get(url, headers=headers, verify=False, timeout=6)
        if cf_loop in [301, 302, 303]:
            print(cf_loop.headers)
            if "CF-Cache-Status: HIT" in cf_loop.headers:
                print("   \033[32m└──+\033[0m Potential redirect loop exploit possible with \033[32m{}\033[0m payload".format(headers))