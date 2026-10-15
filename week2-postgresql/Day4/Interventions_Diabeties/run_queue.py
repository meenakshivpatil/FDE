import service

if __name__ == "__main__":
    result = service.build_queue()
    print(f"Queue rows created: {result['created']}")
    print(f"Queue size (MEDIUM+HIGH): {len(service.get_care_queue(limit=100000))}")
