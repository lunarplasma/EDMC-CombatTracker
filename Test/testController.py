import unittest
from controller import Controller
from datetime import datetime


class TestController(unittest.TestCase):
    def test_gets_proper_dates(self):
        """Tests that logs are filtered by date as expected"""

        # This is a whole bunch of logs, starting from the 26th December to 9th of Jan
        logs = [
            "Journal.201226194838.01.log",
            "Journal.201227094356.01.log",
            "Journal.201228103554.01.log",
            "Journal.201228104525.01.log",
            "Journal.201229121353.01.log",
            "Journal.201229142344.01.log",
            "Journal.201229153655.01.log",
            "Journal.201230165401.01.log",
            "Journal.201230185246.01.log",
            "Journal.201231192004.01.log",
            "Journal.201231205104.01.log",
            "Journal.201230085906.01.log",
            "Journal.201230163526.01.log",
            "Journal.201230195240.01.log",
            "Journal.201231093029.01.log",
            "Journal.201231095050.01.log",
            "Journal.201231141854.01.log",
            "Journal.201231161228.01.log",
            "Journal.210101095506.01.log",
            "Journal.210101113726.01.log",
            "Journal.210101160904.01.log",
            "Journal.210101190626.01.log",
            "Journal.210102091258.01.log",
            "Journal.210102112734.01.log",
            "Journal.210102161913.01.log",
            "Journal.210102161913.01.log",
            "Journal.210102162032.01.log",
            "Journal.210102170348.01.log",
            "Journal.210102170527.01.log",
            "Journal.210102172308.01.log",
            "Journal.210102195352.01.log",
            "Journal.210102195509.01.log",
            "Journal.210102195606.01.log",
            "Journal.210103100524.01.log",
            "Journal.210103162907.01.log",
            "Journal.210103181213.01.log",
            "Journal.210104193618.01.log",
            "Journal.210105190148.01.log",
            "Journal.210106183037.01.log",
            "Journal.210107120304.01.log",
            "Journal.210107161807.01.log",
            "Journal.210107174030.01.log",
            "Journal.210107192239.01.log",
            "Journal.210107204906.01.log",
            "Journal.210108125529.01.log",
            "Journal.210108161820.01.log",
            "Journal.210108163500.01.log",
            "Journal.210108190306.01.log",
            "Journal.210109103558.01.log",
        ]

        # 29th december to 4th jan
        expected_logs = [
            "Journal.201229121353.01.log",
            "Journal.201229142344.01.log",
            "Journal.201229153655.01.log",
            "Journal.201230165401.01.log",
            "Journal.201230185246.01.log",
            "Journal.201231192004.01.log",
            "Journal.201231205104.01.log",
            "Journal.201230085906.01.log",
            "Journal.201230163526.01.log",
            "Journal.201230195240.01.log",
            "Journal.201231093029.01.log",
            "Journal.201231095050.01.log",
            "Journal.201231141854.01.log",
            "Journal.201231161228.01.log",
            "Journal.210101095506.01.log",
            "Journal.210101113726.01.log",
            "Journal.210101160904.01.log",
            "Journal.210101190626.01.log",
            "Journal.210102091258.01.log",
            "Journal.210102112734.01.log",
            "Journal.210102161913.01.log",
            "Journal.210102161913.01.log",
            "Journal.210102162032.01.log",
            "Journal.210102170348.01.log",
            "Journal.210102170527.01.log",
            "Journal.210102172308.01.log",
            "Journal.210102195352.01.log",
            "Journal.210102195509.01.log",
            "Journal.210102195606.01.log",
            "Journal.210103100524.01.log",
            "Journal.210103162907.01.log",
            "Journal.210103181213.01.log",
            "Journal.210104193618.01.log",
        ]

        start_date = datetime(year=2020, month=12, day=29)
        end_date = datetime(year=2021, month=1, day=4)

        results = Controller.filter_logs_by_date(logs,
                                                 start_date=start_date,
                                                 end_date=end_date
                                                 )

        self.assertListEqual(expected_logs, results)


if __name__ == '__main__':
    unittest.main()
